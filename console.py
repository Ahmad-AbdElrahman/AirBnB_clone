#!/usr/bin/python3
import cmd
from datetime import datetime
from models.base_model import BaseModel
from models.user import User


class HBNBCommand(cmd.Cmd):
    intro = "Welcome to the airbnb console.\tType help or ? to list commands.\n"
    prompt = "(hbnb) "
    file = "hbnb.json"  # the JSON file

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, and saves it a JSON file
        """
        classes = {  # FOR TESTING ONLY
            "BaseModel": ["m123"],
            "UserModel": ["m789"],
        }

        args = arg.split()
        cls_name = ""

        if len(args) > 0:
            cls_name = args[0].strip('"')

        if not cls_name:
            print("** class name missing **")
            return

        if cls_name not in classes:
            print("** class doesn't exist **")
            return

        new = cls_name()
        with open(self.file, 'w') as file:
            file.write(new)

        print(f"{classes[cls_name][0]}")

    def do_show(self, arg):
        """
        Prints the string representation of an instance
        based on the class name and uid
        """
        classes: dict[str, list[str]] = {  # FOR TESTING ONLY
            "BaseModel": ["m123", "m456"],
            "UserModel": ["m789", "m159"],
        }

        args: list[str] = arg.split()
        cls_name = ""
        instance_id = ""

        if len(args) > 0:
            cls_name = args[0].strip('"')
        if len(args) > 1:
            instance_id = args[1].strip('"')

        if not cls_name:
            print("** class name missing **")
            return

        if cls_name not in classes:
            print("** class doesn't exist **")
            return

        if not instance_id:
            print("** instance id missing **")
            return

        if instance_id not in classes[cls_name]:
            print("** no instance found **")
            return
        # SHOULD BE REPLACED WITH THE ACTUAL STR REPRESENTATION
        print(
            f"[{cls_name}] ({instance_id}) "
            f"{{'first_name': 'Betty', 'id': '{instance_id}', "
            f"'created_at': {datetime(2024, 10, 2, 3, 10, 25, 903293)}, "
            f"'updated_at': {datetime(2024, 10, 2, 3, 11, 3, 49401)}}}",
        )

    def do_all(self, arg):
        """
        Prints all string representation of all instances
        based or not on the class name
        """
        pass

    def do_update(self, arg):
        """
        Updates an instance based on the class name and uid
        by adding or updating attribute (save the change into the JSON file)
        """
        pass

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and uid
        (save the change into the JSON file)
        """
        pass

    def do_EOF(self, arg):
        'Close the AirBnB console, and exit the program.'
        return True

    def do_quit(self, arg):
        'Close the AirBnB console, and exit the program.'
        print('Quit')
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
