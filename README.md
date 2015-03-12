![DoDo](https://github.com/atmb4u/dodo/blob/master/logo.png?raw=true)
DoDo - Task Management for Hackers
----------------------------------

Dodo is an easily maintainable task list for version controlled projects and hackers. We can call `dodo`  a ticket tracking inside the repo itself.
Tasks are called as *DoDo*, and __your goal is to make DoDo's extinct.__


###Getting Started

```python
pip install dodopie
```

###Initializing
```python
dodo init
```
    Options

    dodo init -f [dodo filename]

### List all Tasks
```python
dodo l
```

### Propose a new Task
```bash
dodo propose -u atmb4u -d "dodo new version"
```

### Accept a Tasks
```bash
dodo accept --id 2 -u atmb4u -d "dodo new version"
```

### Reject a proposed Tasks
```bash
dodo reject --id 2 -u atmb4u
```

### Work on a new Tasks
```bash
dodo workon --id 2 -u atmb4u
```

### Mark a task as Finished
```bash
dodo finish --id 1 -u atmb4u -d "dodo new version"
```

## Authors
atmb4u [at] gmail [dot] com