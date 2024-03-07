#!/usr/bin/python3
import re
import cmd
from models.base_model import BaseModel
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.state import State
from models.city import City
from models.user import User
from models import storage

classes = {
    'BaseModel': BaseModel,
    'Amenity': Amenity,
    'Review': Review,
    'Place': Place,
    'State': State,
    'City': City,
    'User': User,
}


class HBNBCommand(cmd.Cmd):
    intro = "Welcome to the airbnb console.\tType help or ? to list commands.\n"
    prompt = "(hbnb) "
    file = "hbnb.json"

    def default(self, line):
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
            print("** invalid method **")
            return

        if method in ("all", "create", "count"):
            commands[method](cls_name)
            return

        cls_id = cmd[2]
        args = f"{cls_name} {cls_id}"
        if method in ("show", "destroy"):
            commands[method](args, check_id=True)
            return

        cls_id = cmd[2].split(',')[0]
        attr_name = cmd[2].split(',')[1] if len(cmd[2].split(',')) > 1 else ""
        attr_value = cmd[2].split(',')[2] if len(cmd[2].split(',')) > 2 else ""
        args = f"{cls_name} {cls_id} {attr_name} {attr_value}"
        if method == "update":
            commands[method](
                args, check_id=True, check_attr_name=True, check_attr_value=True
            )
            return

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, and saves it a JSON file.
        """
        args = validated_args(arg)
        if not args:
            return

        cls_name = args["cls_name"]
        model = classes[cls_name]()
        model.save()
        print(model.id)

    def do_show(self, arg, check_id=True):
        """
        Prints the string representation of an instance
        based on the class name and uid.
        """
        args = validated_args(arg, check_id=check_id)
        if not args:
            return

        cls_name = args["cls_name"]
        cls_id = args["cls_id"]

        all_objs = storage.all()
        key = f"{cls_name}.{cls_id}"  # key = "User.45d0-98ed-438d-92e4-d4a2"
        obj = all_objs.get(key)

        if obj is None:
            print("** no instance found **")
            return
        print(obj)

    def do_all(self, arg):
        """
        Prints all string representation of all instances
        based or not on the class name.
        """
        args = arg.split()
        cls_name = args[0].strip('"') if args else ""

        if cls_name and cls_name not in classes:
            print("** class doesn't exist **")
            return

        all_objs = storage.all()
        arr = [
            value.__str__()
            for value in all_objs.values()
            if not cls_name or value.__class__.__name__ == cls_name
        ]
        print(arr)

    def do_update(
        self, arg, check_id=True, check_attr_name=True, check_attr_value=True
    ):
        """
        Updates an instance based on the class name and uid
        by adding or updating attribute (save the change into the JSON file).

        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        args = validated_args(
            arg,
            check_id=check_id,
            check_attr_name=check_attr_name,
            check_attr_value=check_attr_value,
        )
        if not args:
            return

        cls_name = args["cls_name"]
        cls_id = args["cls_id"]
        attr_name = args["attr_name"]
        attr_value = args["attr_value"]

        all_objs = storage.all()
        key = f"{cls_name}.{cls_id}"
        obj = all_objs.get(key)

        if obj is None:
            print("** no instance found **")
            return

        setattr(obj, attr_name, attr_value)
        obj.save()

    def do_destroy(self, arg, check_id=True):
        """
        Deletes an instance based on the class name and uid
        (save the change into the JSON file).
        """
        args = validated_args(arg, check_id=check_id)
        if not args:
            return

        cls_name = args["cls_name"]
        cls_id = args["cls_id"]

        all_objs = storage.all()
        key = f"{cls_name}.{cls_id}"
        removed_obj = all_objs.pop(key, None)
        if removed_obj is None:
            print("** no instance found **")
            return
        storage.save()

    def do_count(self, arg):
        """
        Count the number of instance for each class.
        """
        args = validated_args(arg)
        if not args:
            return

        nm_instances = 0
        all_objs = storage.all()

        if arg == "all":
            for obj in all_objs.values():
                nm_instances += 1
            print(nm_instances)
            return

        for obj in all_objs.values():
            if obj.__class__.__name__ == args["cls_name"]:
                nm_instances += 1
        print(nm_instances)

    def do_EOF(self, arg):
        """
        Close the AirBnB console, and exit the program.
        """
        print('EOF')
        return True

    def do_quit(self, arg):
        """
        Close the AirBnB console, and exit the program.
        """
        print('Quit')
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


def validated_args(arg, **kwargs):
    args = arg.split()
    cls_name = args[0].strip('"') if args else ""
    if not cls_name:
        print("** class name missing **")
        return
    if cls_name not in classes and cls_name != "all":
        print("** class doesn't exist **")
        return
    cls_id = args[1].strip('"\'') if len(args) > 1 else ""
    if not cls_id and kwargs.get("check_id", False):
        print("** instance id missing **")
        return
    attr_name = args[2].strip('"') if len(args) > 2 else ""
    if not attr_name and kwargs.get("check_attr_name", False):
        print("** attribute name missing **")
        return
    attr_value = args[3].strip('"') if len(args) > 3 else ""
    if not attr_value and kwargs.get("check_attr_value", False):
        print("** value missing **")
        return

    return {
        "cls_name": cls_name,
        "cls_id": cls_id,
        "attr_name": attr_name,
        "attr_value": attr_value,
    }


if __name__ == '__main__':
    HBNBCommand().cmdloop()
