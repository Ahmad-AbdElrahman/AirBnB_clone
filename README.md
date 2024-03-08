# The AirBnB Cloned Website

![project_logo](./assets/hbnb.png)

## Introduction
The AirBnB clone is a full-stack web application that integrats a database storage, a back-end API, and a front-end interface.
This project is part of the (Alx) Holberton School Software Engineering program.

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

The **Console** serves as the core foundation for this project. Building a CLI allows us to directly interact with the system, receive immediate feedback on actions and understand how commands translate into program logic. This makes the **Console** a valuable tool for testing and debugging our code efficiently.

The console offers the following functionalities:

- Creating new instances of various classes.
- Showing information about existing instances based on class and id.
- Updating existing instances by adding or modifying their attributes.
- Deleting existing instances from the storage.
- Counting the number of instances for each class.

Examples of using the console both interactively and non-interactively:

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

- Testing the console file:

```sh
$ python3 -m unittest tests.test_console
```

- Testing specific model file:

```sh
$ python3 -m unittest tests.test_models.<test_filename>
```

- Testing specific test class:

```sh
$ python3 -m unittest tests.<test_folder>.<test_filename>.<test_class>
```

- Testing specific test case:

```sh
$ python3 -m unittest tests.<test_folder>.<test_filename>.<test_class>.<test_case>
```

- Non-interactive mode: 
```sh
$ echo "python3 -m unittest discover tests" | bash
```
