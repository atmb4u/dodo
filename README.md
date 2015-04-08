![DoDo](https://github.com/atmb4u/dodo/blob/master/logo.png?raw=true)
DoDo - Task Management for Hackers
----------------------------------

Dodo is an easily maintainable task list for version controlled projects and hackers. We can call `dodo`  a ticket tracking inside the repo itself.
Tasks are called as *DoDo*, and __your goal is to make DoDos extinct.__

In the latest version, username is automatically populated from the system username if not passed explicitly. And the usage flow has been stripped down so as to take the ease of use to the next level


## Getting Started

```python
pip install dodopie
# use sudo if you want to install dodo globally
# sudo pip install dodopie
```

### Initializing

```python
dodo init
```
    Options

    dodo init -f [dodo filename]


### Basic WorkFlow


```python
dodo add "New Task"  # add a new DoDo
```
``` python
dodo l  # list all dodo tasks
> ID	Status		Date(-t)	    Owner(-u)		Description (-d)
> 1	    [+]		    1 minute ago	(atm)		    New Task
```
```python
dodo workon 1  # mark DoDo #1 as working on
```
```python
dodo finish 1  # mark DoDo #1 as finished
```
```python
dodo l
> ID	Status		Date(-t)	    Owner(-u)		Description (-d)
> 1	    [.]		    1 minute ago	(atm)		    New Task
```

## Detailed Documentation

### List all Tasks
```python
dodo l
```

### Propose a new Task
```bash

# simple version
dodo add "This is a new task"

# verbose version
dodo c -u atmb4u -d "dodo new version"
dodo add -u atmb4u -d "dodo new version"
dodo propose -u atmb4u -d "dodo new version"
```

### Accept a Tasks
```bash

# simple version
dodo accept 2

# verbose version

dodo accept --id 2 -u atmb4u -d "dodo new version"
```

### Reject a proposed Tasks
```bash

# simple version
dodo reject 2

# verbose version
dodo reject --id 2 -u atmb4u
```

### Work on a new Tasks
```bash

# simple version
dodo workon 2

# verbose version
dodo workon --id 2 -u atmb4u
```

### Mark a task as Finished
```bash

# simple version
dodo finish 1

# verbose version
dodo finish --id 1 -u atmb4u -d "dodo new version"
```

### Remove a Task
```bash
dodo remove 1
```

### Export Tasks
```bash
dodo export -o filename.json
# will export all the tasks to filename.json
# Can use --output as well

dodo export
# will print all the tasks in json format
```

### Import Tasks
```bash
dodo import -i filename.json
# will import all the tasks from filename.json
# Can use --input as well

Sample Input File Format: [{"id":1, "description":"Read Docs Now", "entry":"20150405T020324Z",
"status":"pending", "uuid":"1ac1893d-db66-40d7-bf67-77ca7c51a3fc","urgency":"0"}]
```


## Authors
atmb4u [at] gmail [dot] com


Thanks to IanCal, GuyOnTheInterweb, elrac1, iambeard for the **super creative** suggestions in [reddit](http://www.reddit.com/r/coding/comments/2zgie7/dodo_task_management_for_developers/)
