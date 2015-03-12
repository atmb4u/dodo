#!/usr/bin/env python
import argparse
import re
import time
import os


DODO_FILE = os.path.join(os.getcwd(), 'DODO')
VERSION = "0.94"


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
    file_inst.close()
    return do_dict


def dodo_unload(final_do_base):
    content = ""
    for key, value in final_do_base.iteritems():
        content += "#%s [[%s]] <<%s>> ((%s)) {{%s}}\n" % (value["id"], value["status"], value["time"],
                                                          value["user"], value["description"])
    dodo_write(content, "w")


def dodo_init(args):
    file_name = args.file or DODO_FILE
    try:
        try:
            open(file_name, "r")
            print "DoDo already exist."
        except IOError:
            file_inst = open(file_name, "w")
            file_inst.close()
            print "Successfully initialized DoDo"
    except IOError:
        print "Cannot create file in the following location: %s" % file_name


def dodo_write(content, mode="a"):
    global DODO_FILE, do_base
    file_inst = open(DODO_FILE, mode)
    file_inst.write(content)
    file_inst.close()
    print "DoDo updated."


def dodo_change_status(args, mod_do_base, status):
    if not args.id:
        print "ID (-id) can't be empty"
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
            print "Description (-d) can't be empty"
            return
        do_id = str(len(mod_do_base) + 1)
        do_description = args.desc
        do_user = args.user
        do_time = args.time or time.strftime("%d-%m-%y %H:%M", time.localtime())
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
    if args.operation in ["add", "propose", "c"]:
        do_id = str(len(do_base) + 1)
        do_description = args.desc
        do_user = args.user
        do_time = args.time or time.strftime("%d-%m-%y %H:%M", time.localtime())
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
            print "No task with id %s" % args.id
        dodo_unload(do_base)
    return


def dodo_list():
    global do_base
    print "%s%sID\tStatus\t\tDate(-t)\tOwner(-u)\t\tDescription (-d)\n%s" % (TerminalColors.BOLD,
                                                                             TerminalColors.UNDERLINE,
                                                                             TerminalColors.END)
    for key, value in do_base.iteritems():
        color = TerminalColors.YELLOW
        if value["status"] == ".":
            color = TerminalColors.GREEN
        elif value["status"] in ["-", 'x']:
            color = TerminalColors.RED
        elif value["status"] == "#":
            color = TerminalColors.YELLOW
        elif value["status"] == "+":
            color = TerminalColors.BLUE
        user = value["user"] if value["user"] != "None" else "anonymous"
        print "%s%s\t[%s]\t\t%s\t(%s)\t\t%s%s" % (color, value["id"], value["status"], value["time"],
                                                  user, value["description"], TerminalColors.END)
    print "%sAvailable Operations: c accept propose reject workon finish remove d\n" \
          "Available Options: -id -d(description) -u(user) -t(time) -f(file)\n" \
          "Status: + proposed - rejected * accepted # working . complete%s" % (
              TerminalColors.BOLD, TerminalColors.END)


def dodo_switch(args):
    global do_base
    if args.operation == "init":
        dodo_init(args)
    elif args.operation in ['add', 'propose', 'accept', 'reject', 'workon', 'finish', 'remove', "c", "d"]:
        dodo_add(args)
    else:
        dodo_list()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", type=str,
                        help="List all existing dodos add, propose, accept, reject, workon, finish, remove")
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
    arguments = parser.parse_args()
    global do_base
    do_base = {}
    if arguments.operation == "init":
        dodo_init(arguments)
    else:
        do_base = dodo_load(arguments)
        dodo_switch(arguments)
