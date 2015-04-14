#!/usr/bin/env python
import argparse
import calendar
import json
import re
import time
import os
from datetime import datetime
from time import mktime


DODO_FILE = os.path.join(os.getcwd(), 'DODO')
VERSION = "0.98"
username = os.path.split(os.path.expanduser('~'))[-1]


class TerminalColors(object):
    """
    Color class for listing out dodos
    """
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    def __init__(self):
        pass

statuses = {
    '+': 'add',
    '*': 'accepted',
    '-': 'rejected',
    '#': 'working',
    '.': 'complete'
}


def pretty_date(date_string):
    timestamp = calendar.timegm((datetime.strptime(date_string, "%d-%m-%y %H:%M")).timetuple())
    date = datetime.fromtimestamp(timestamp)
    diff = datetime.now() - date
    s = diff.seconds
    if diff.days > 7 or diff.days < 0:
        return date.strftime('%d %b %y')
    elif diff.days == 1:
        return '1 day ago'
    elif diff.days > 1:
        return '{} days ago'.format(diff.days)
    elif s <= 1:
        return 'just now'
    elif s < 60:
        return '{} seconds ago'.format(s)
    elif s < 120:
        return '1 minute ago'
    elif s < 3600:
        return '{} minutes ago'.format(s/60)
    elif s < 7200:
        return '1 hour ago'
    else:
        return '{} hours ago'.format(s/3600)


def parse_dodo(line):
    if line:
        do_id = re.search("#\d+", line).group()[1:]
        do_status = re.search(r'\[\[\W+\]\]', line).group()[2:-2]
        do_time = re.search(r'(<<.+>>)', line)
        do_description = re.search(r'({{.+}})', line)
        if do_time:
            do_time = do_time.group().replace("<<", "").replace(">>", "")
        do_user = re.search(r'(\(\(.+\)\))', line)
        if do_user:
            do_user = do_user.group().replace("((", "").replace("))", "")
        if do_description:
            do_description = do_description.group().replace("{{", "").replace("}}", "")
        return {
            "id": do_id,
            "time": do_time,
            "user": do_user,
            "status": do_status,
            "description": do_description
        }


def dodo_load(args):
    global DODO_FILE
    do_dict = {}
    DODO_FILE = args.file or DODO_FILE
    with open(DODO_FILE, 'r') as file_inst:
        contents = file_inst.readlines()
        for content in contents:
            do_data = parse_dodo(content)
            do_dict.update({do_data["id"]: do_data})
    return do_dict


def dodo_unload(final_do_base):
    content = ""
    for key, value in sorted(iter(final_do_base.items()), key=lambda key_value: key_value[0]):
        content += "#%s [[%s]] <<%s>> ((%s)) {{%s}}\n" % (value["id"], value["status"], value["time"],
                                                          value["user"], value["description"])
    dodo_write(content, "w")


def dodo_init(args):
    file_name = args.file or DODO_FILE
    try:
        try:
            open(file_name, "r")
            print("DoDo already exist.")
        except IOError:
            file_inst = open(file_name, "w")
            file_inst.close()
            print("Successfully initialized DoDo")
    except IOError:
        print("Cannot create file in the following location: %s" % file_name)


def dodo_write(content, mode="a"):
    global DODO_FILE, do_base
    file_inst = open(DODO_FILE, mode)
    file_inst.write(content)
    file_inst.close()
    dodo_list()


def dodo_change_status(args, mod_do_base, status):
    if not args.id:
        print("ID (-id) can't be empty. May be try creating the task first")
        return
    do_entry = mod_do_base.get(args.id)
    if do_entry:
        do_entry["status"] = status
        if args.desc:
            do_entry["description"] = args.desc
        if args.user:
            do_entry["user"] = args.user
        if args.time:
            do_entry["time"] = args.time
    else:
        if not args.desc:
            print("Description (-d) can't be empty")
            return
        do_id = str(len(mod_do_base) + 1)
        do_description = args.desc
        do_user = args.user
        do_time = args.time or time.strftime("%d-%m-%y %H:%M", time.gmtime())
        mod_do_base[do_id] = {
            "id": do_id,
            "time": do_time,
            "user": do_user,
            "status": status,
            "description": do_description
        }
    dodo_unload(mod_do_base)
    return


def dodo_add(args):
    """
    + add/proposed
    * accepted
    - rejected
    # working
    . complete
    """
    global username
    do_user = args.user or username
    if args.operation in ["add", "propose", "c"]:
        if args.id:
            print("Error: DoDo assigns id for you.")
            exit()
        do_id = str(len(do_base) + 1)
        do_description = args.desc
        do_time = args.time or time.strftime("%d-%m-%y %H:%M", time.gmtime())
        do_base[do_id] = {
            "id": do_id,
            "time": do_time,
            "user": do_user,
            "status": "+",
            "description": do_description
        }
        dodo_unload(do_base)
    elif args.operation == "accept":
        dodo_change_status(args, do_base, "*")
    elif args.operation == "reject":
        dodo_change_status(args, do_base, "-")
    elif args.operation == "workon":
        dodo_change_status(args, do_base, "#")
    elif args.operation == "finish":
        dodo_change_status(args, do_base, ".")
    elif args.operation in ["remove" or "d"]:
        try:
            do_base.pop(args.id)
        except KeyError:
            print("No task with id %s" % args.id)
        dodo_unload(do_base)
    return


def dodo_list():
    global do_base
    print("%s%sID\tStatus\t\tDate(-t)\tOwner(-u)\t\tDescription (-d)\n%s" % (TerminalColors.BOLD,
                                                                             TerminalColors.UNDERLINE,
                                                                             TerminalColors.END))
    for key, value in sorted(iter(do_base.items()), key=lambda key_value1: key_value1[0]):
        color = TerminalColors.YELLOW
        if value["status"] == ".":
            color = TerminalColors.GREEN
        elif value["status"] in ["-", 'x']:
            color = TerminalColors.RED
        elif value["status"] == "#":
            color = TerminalColors.UNDERLINE + TerminalColors.YELLOW
        elif value["status"] == "+":
            color = TerminalColors.BLUE
        user = value["user"] if value["user"] != "None" else "anonymous"
        human_time = pretty_date(value["time"])
        print("%s%s\t[%s]\t\t%s\t(%s)\t\t%s%s" % (color, value["id"], value["status"], human_time,
                                                  user, value["description"], TerminalColors.END))
    print("\n%sAvailable Operations: c accept propose reject workon finish remove d\n" \
          "Available Options: -id -d(description) -u(user) -t(time) -f(file)\n" \
          "Status: + proposed - rejected * accepted # working . complete%s" % (
              TerminalColors.BOLD, TerminalColors.END))


def dodo_import(args):
    """
    Sample import JSON format (same as taskwarrior export format)
    {"id":1,"description":"Read Docs Now","entry":"20150405T020324Z","status":"pending",
    "uuid":"1ac1893d-db66-40d7-bf67-77ca7c51a3fc","urgency":"0"}
    """
    global username
    do_user = args.user or username
    json_file = args.input
    json_source = json.loads(open(json_file).read())
    for task in json_source:
        do_id = str(len(do_base) + 1)
        do_description = task["description"]
        utc_time = time.strptime(task["entry"], "%Y%m%dT%H%M%S%fZ")
        do_time = time.strftime("%d-%m-%y %H:%M", utc_time)
        do_status = "+"
        if task["status"] == "pending":
            do_status = "+"
        if task["status"] == "completed":
            do_status = "."
        do_base[do_id] = {
            "id": do_id,
            "time": do_time,
            "user": do_user,
            "status": do_status,
            "description": do_description
        }
    dodo_unload(do_base)
    print("Imported %d tasks successfully" % len(json_source))


def dodo_export(args):
    """
    {"id":1,"description":"Read Docs Now","entry":"20150405T020324Z","status":"pending",
    "uuid":"1ac1893d-db66-40d7-bf67-77ca7c51a3fc","urgency":"0"}
    Time is in UTC
    """
    dodo_data = []
    for instance in sorted(list(do_base.values()), key=lambda value: value["id"]):
        dodo_data.append({
            "id": instance["id"],
            "time": instance["time"],
            "user": instance["user"],
            "status": statuses[instance["status"]],
            "description": instance["description"]
        }
        )
    if args.output:
        try:
            file_name = args.output
            file_inst = open(file_name, "w")
            file_inst.write(json.dumps(dodo_data))
            file_inst.close()
            print("%sExported DODO to %s%s" % \
                  (TerminalColors.GREEN, file_name, TerminalColors.END))
        except IOError:
            print("%sExport failed; Check for permission to create/edit %s%s" % \
                  (TerminalColors.RED, args.output, TerminalColors.END))
    else:
        print("%sUse -e or --export to <filename.json> to export to a file.%s" % \
              (TerminalColors.YELLOW, TerminalColors.END))
        print("%s" % TerminalColors.GREEN)
        print(dodo_data)
        print("%s" % TerminalColors.END)


def dodo_switch(args):
    global do_base
    if args.operation == "init":
        dodo_init(args)
    elif args.operation in ['add', 'propose', 'accept', 'reject', 'workon', 'finish', 'remove', "c", "d"]:
        dodo_add(args)
    elif args.operation == 'import':
        dodo_import(args)
    elif args.operation == 'export':
        dodo_export(args)
    else:
        dodo_list()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", type=str,
                        help="List all existing dodos add, propose, accept, reject, workon, finish, remove")
    parser.add_argument("quick_access", type=str, nargs='?', default='',
                        help="Task ID for a operation or Description for the new task")
    parser.add_argument("-d", "--desc", "--description", type=str,
                        help="Task Description")
    parser.add_argument("-u", "--user", type=str,
                        help="User ID")
    parser.add_argument("-t", "--time", type=str,
                        help="Expected/Completed Date - 11-03-2015")
    parser.add_argument("--id", type=str,
                        help="List all existing dodos")
    parser.add_argument("-f", "--file", type=str,
                        help="DODO filename")
    parser.add_argument("-i", "--input", type=str,
                        help="Import from JSON file")
    parser.add_argument("-o", "--output", type=str,
                        help="Export to JSON file")
    arguments = parser.parse_args()
    quick_access = arguments.quick_access
    print(quick_access)
    if quick_access:
        if arguments.quick_access.isdigit():
            arguments.id = quick_access
        elif quick_access:
            arguments.desc = quick_access
    global do_base
    do_base = {}
    if arguments.operation == "init":
        dodo_init(arguments)
    else:
        do_base = dodo_load(arguments)
        dodo_switch(arguments)
