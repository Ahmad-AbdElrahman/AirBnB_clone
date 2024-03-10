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


class HBNBConsole(cmd.Cmd):
    """
    Command-line interface for interacting with BaseModel instances.

    This class provides a user interface for interacting with the system
    through text commands. It parses user input, validates arguments, and
    delegates tasks to appropriate methods for CRUD (Create, Read, Update,
    Delete) operations on BaseModel instances.

    The class inherits from `cmd.Cmd` from the `cmd` module, providing
    functionalities for handling user input and interactions within the
    console.
    """

    prompt = "(hbnb) "
    file = "hbnb.json"

    def default(self, line):
        """
        Handles cases where user commands are not recognized by HBNBConsole.

        This method is invoked when the user enters a command
        that doesn't match any of the defined functionalities in HBNBConsole.
        It checks for a pattern matching "<class_name>.<method>(<args>)"
        and attempts to call the corresponding do_* method if valid.
        Otherwise, it prints an error message.

        Args:
        -   line (str): The user input command string.
        """
        commands = {
            "create": self.do_create,
            "count": self.do_count,
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update,
        }

        pattern = r"^(\w+)\.(\w+)\((.*)\)$"
        matched = re.match(pattern, line)

        if not matched:
            super().default(line)
            return

        cmd = matched.groups()
        args = ""
        method = cmd[1]
        cls_name = cmd[0]

        if method not in commands:
            print(error_messages["no_method"])
            return

        if method in ("all", "create", "count"):
            commands[method](cls_name)
            return

        obj_id = cmd[2]
        args = f"{cls_name} {obj_id}"
        if method in ("show", "destroy"):
            commands[method](args, check_id=True)
            return

        obj_id = cmd[2].split(',')[0]
        attr_name = cmd[2].split(',')[1] if len(cmd[2].split(',')) > 1 else ""
        attr_value = cmd[2].split(',')[2] if len(cmd[2].split(',')) > 2 else ""
        args = f"{cls_name} {obj_id} {attr_name} {attr_value}"
        if method == "update":
            commands[method](
                args, check_id=True, check_attr_name=True, check_attr_val=True
            )
            return

    def do_create(self, arg):
        """
        Creates a new instance, and saves it a JSON file.

        Args:
        -   arg (str): The user input argument (command to be interpreted).

        Return:
        -   None (prints the created instance id on success).

        Raises:
        -   None (prints error messages to the console).
        """
        args = validate(arg)
        if not args:
            return

        cls_name = args["cls_name"]
        instance = classes[cls_name]()
        instance.save()
        print(instance.id)

    def do_show(self, arg, check_id=True):
        """
        Prints the string representation of an instance
        based on the class name and its id.

        Args:
        -   arg (str): The user input argument (command to be interpreted).
        -   check_id (bool):
                If True, checks if an instance id is provided.
                (defaults to True)

        Return:
        -   None (prints the instance id on success).

        Raises:
        -   None (prints error messages to the console).
        """
        args = validate(arg, check_id=check_id)
        if not args:
            return

        cls_name = args["cls_name"]
        obj_id = args["obj_id"]
        all_objs = storage.all()
        key = f"{cls_name}.{obj_id}"
        obj = all_objs.get(key)

        if obj is None:
            print(error_messages["no_obj"])
            return
        print(obj)

    def do_all(self, arg):
        """
        Prints a string representation of all instances.

        Args:
        -   arg (str): The user input argument (command to be interpreted).

        Return:
        -   None (prints all the instances or empty []).

        Raises:
        -   None (prints error messages to the console).
        """
        args = arg.split()
        cls_name = args[0].strip("'\"") if args else ""

        if cls_name and cls_name not in classes:
            print("** class doesn't exist **")
            return

        all_objs = storage.all()
        obj_list = [
            obj.__str__()
            for obj in all_objs.values()
            if not cls_name or obj.__class__.__name__ == cls_name
        ]
        print(obj_list)

    def do_update(
        self, arg, check_id=True, check_attr_name=True, check_attr_val=True
    ):
        """
        Updates an instance based on the class name and its id.

        Args:
        -   arg (str): The user input argument (command to be interpreted).
        -   check_id (bool):
                If True, checks if an instance id is provided.
                (defaults to True)
        -   check_attr_name (bool):
                If True, checks if an attribute name is provided.
                (defaults to True)
        -   check_attr_val (bool):
                If True, checks if an attribute value is provided.
                (defaults to True)

        Raises:
        -   None (prints error messages to the console).
        """
        args = validate(
            arg,
            check_id=check_id,
            check_attr_name=check_attr_name,
            check_attr_val=check_attr_val,
        )
        if not args:
            return

        cls_name = args["cls_name"]
        obj_id = args["obj_id"]
        attr_name = args["attr_name"]
        attr_value = args["attr_value"]

        all_objs = storage.all()
        key = f"{cls_name}.{obj_id}"
        obj = all_objs.get(key)

        if obj is None:
            print(error_messages["no_obj"])
            return

        setattr(obj, attr_name, attr_value)
        obj.save()

    def do_destroy(self, arg, check_id=True):
        """
        Deletes an instance based on the class name and provided instance id
        (saves the change into the JSON file).

        Args:
        -   arg (str): The user input argument (command to be interpreted).
        -   check_id (bool): Checks if an instance id is provided
                             (defaults to True)
        """
        args = validate(arg, check_id=check_id)
        if not args:
            return

        cls_name = args["cls_name"]
        obj_id = args["obj_id"]

        all_objs = storage.all()
        key = f"{cls_name}.{obj_id}"
        removed_obj = all_objs.pop(key, None)
        if removed_obj is None:
            print(error_messages["no_obj"])
            return

        storage.save()
        """
        # confirmation logic:
        answered = False
        while not answered:
            confirm = input(
                f"Are you sure you want to delete "
                f"this instance [{cls_name}.{obj_id}]? (y/n): "
            )
            if confirm.lower() in ('yes', 'y'):
                storage.save()
                print(f"{cls_name}.{obj_id} destroyed.")
                answered = True
            elif confirm.lower() in ('no', 'n'):
                all_objs[key] = removed_obj
                print(f"action canceled.")
                answered = True
            else:
                all_objs[key] = removed_obj
                print("** invalid option **")
            """

    def do_count(self, arg):
        """
        Count the number of instance for each class.

        Args:
        -   arg (str): The user input argument (command to be interpreted).
        """
        args = validate(arg)
        if not args:
            return

        nm_instances = 0
        all_objs = storage.all()
        for obj in all_objs.values():
            nm_instances += (
                1
                if arg == "all" or obj.__class__.__name__ == args["cls_name"]
                else 0
            )
        print(nm_instances)

    def do_reset(self, arg):
        """
        Resets the console screen.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def do_EOF(self, arg):
        """
        Exit the program using EOF (Ctrl+D)
        """
        print()
        return True

    def do_quit(self, arg):
        """
        Quit command to exit the program
        """
        return True

    def emptyline(self):
        """
        Do nothing on empty line.
        """
        pass

    def do_help(self, arg):
        """
        Show information about current commands.
        """
        super().do_help(arg)


def validate(arg, **kwargs):
    """
    Validates user input arguments for the HBNBConsole methods.

    This function parses the user input arguments (`arg`) and performs
    various checks based on the provided keyword arguments (`kwargs`).

    Args:
    -   arg (str): The user input argument (command to be interpreted).
    -   **kwargs (dict): Keyword arguments specifying additional validations.
            - check_id (bool):
                If True, checks if an instance id is provided.
                (defaults to False)
            - check_attr_name (bool):
                If True, checks if an attribute name is provided.
                (defaults to False)
            - check_attr_val (bool):
                If True, checks if an attribute value is provided.
                (defaults to False)

    Returns:
    -   dict: A (dict) containing parsed arguments on successful validation,
              (None) otherwise.

    Raises:
    -   None (prints error messages to the console).
    """
    args: list[str] = arg.split()
    cls_name = args[0].strip("'\"") if args else ""
    if not cls_name:
        print(error_messages["no_cls_name"])
        return
    if cls_name not in classes and cls_name != "all":
        print(error_messages["no_cls"])
        return

    obj_id = args[1].strip("'\"") if len(args) > 1 else ""
    if not obj_id and kwargs.get("check_id", False):
        print(error_messages["no_obj_id"])
        return

    # logic to update using a dictionary like as input
    attributes = ""
    if len(args) > 2:
        attributes = args[2]
    if len(args) > 3:
        attributes = ''.join(args[2:])
    dict_pattern = r"^{([^:]+?):\s*(.*?)}.*$"
    matched = re.search(dict_pattern, attributes)
    if matched:
        attr_name, attr_value = matched.groups()
        attr_name = attr_name.strip("{'\":")
        attr_value = attr_value.strip("'\"}")
    else:
        attr_name = args[2].strip("{'\":") if len(args) > 2 else ""
        attr_value = args[3].strip("'\"}") if len(args) > 3 else ""

    if not attr_name and kwargs.get("check_attr_name", False):
        print(error_messages["no_attr_name"])
        return

    if not attr_value and kwargs.get("check_attr_val", False):
        print(error_messages["no_attr_val"])
        return

    return {
        "obj_id": obj_id,
        "cls_name": cls_name,
        "attr_name": attr_name,
        "attr_value": attr_value,
    }


if __name__ == '__main__':
    HBNBConsole().cmdloop()
