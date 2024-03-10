#!/usr/bin/python3
"""
This module provides a command-line interface (CLI) for interacting with
the AirBnB project models representing various methods for managing
the system. It allows users to apply CRUD operations
on the instances through the console.

The console offers the following functionalities:

- Creating new instances of various classes.
- Showing information about existing instances based on class and id.
- Updating existing instances by adding or modifying their attributes.
- Deleting existing instances from the storage.
- Counting the number of instances for each class.
"""
import os
import re
import cmd
from typing import TypedDict
from models import storage
from models import classes


# for auto-completion
class ErrorMessages(TypedDict):
    no_method: str
    no_cls: str
    no_cls_name: str
    no_obj_id: str
    no_obj: str
    no_attr_name: str
    no_attr_val: str


error_messages: ErrorMessages = {
    "no_method": "** invalid method **",
    "no_cls": "** class doesn't exist **",
    "no_cls_name": "** class name missing **",
    "no_obj_id": "** instance id missing **",
    "no_obj": "** no instance found **",
    "no_attr_name": "** attribute name missing **",
    "no_attr_val": "** value missing **",
}


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb)"
    file = "hbnb.json"
    classes = [
        "BaseModel",
        "User",
        "State",
        "City",
        "Amenity",
        "Place",
        "Review",
    ]

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def emptyline(self):
        """DO nothing upon receving an empty line."""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
