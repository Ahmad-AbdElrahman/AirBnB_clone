# AirBnB Clone

![project_logo](./assets/hbnb.png)

## Introduction

<br>

## Get Started

<br>

Start by cloning this project:
```sh
git clone https://github.com/AhmadYousif89/AirBnB_clone.git
cd AirBnB_clone
``` 

## Project Overview

<br>

This is an overview diagram representing the project workflow.

![diagram](./assets/diagram.png)

The project consist of two major parts:
1. Server side (back-end)
2. Client side (front-end)

### The Console

<br>

- Interactive mode:

```sh
$ ./console.py
Welcome to the airbnb console.  Type help or ? to list commands.

(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update

(hbnb) help create

	Creates a new instance of BaseModel, and saves it a JSON file

(hbnb) quit
Quit
$
```

- Non-interactive mode:

```sh
$ echo 'help' | ./console.py
Welcome to the airbnb console.  Type help or ? to list commands.

(hbnb) 
Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update

(hbnb)
$
```

```sh
$ echo 'help create' | ./console.py
Welcome to the airbnb console.  Type help or ? to list commands.

(hbnb) 
        Creates a new instance of BaseModel, and saves it a JSON file
        
(hbnb)
$
```

```sh
$ echo 'quit' > test_quit
$ echo 'help create' | ./console.py < test_quit
Welcome to the airbnb console.  Type help or ? to list commands.

(hbnb) 
        Creates a new instance of BaseModel, and saves it a JSON file
        
(hbnb) Quit
$
```

### The Storage Engine

<br>
TODO

## Testing

<br>

- Testing all files:

```sh
$ python3 -m unittest discover tests
```

- Testing specific file:

```sh
$ python3 -m unittest tests/<folder>/<filename>
```

- Non-interactive mode: 
```sh
$ echo "python3 -m unittest discover tests" | bash
```
