#!/usr/bin/python3
"""Define the FileStorage class module"""
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review


class FileStorage:
    """Manage serialization and deserialization of class instances."""

    __file_path = "hbnb.json"
    __objects = {}

    def all(self):
        """
        Returns the dictionary __objects

        Returns:
            dict: A dictionary containing all objects stored in the __objects.
        """
        return self.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id

        Args:
        -   obj (BaseModel): The object to be added.
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path)
        """
        with open(self.__file_path, 'w') as f:
            _dict = {k: v.to_dict() for k, v in self.__objects.items()}
            json.dump(_dict, f)

    def reload(self):
        """
        Deserializes the JSON file to objects
        (only if the JSON file (__file_path) exists; otherwise, do nothing)
        (If the file doesn't exist, no exception should be raised)
        """
        classes = {
            'BaseModel': BaseModel,
            'Amenity': Amenity,
            'User': User,
            'City': City,
            'State': State,
            'Place': Place,
            'Review': Review,
        }

        try:
            with open(self.__file_path) as f:
                _dict = json.loads(f.read())
                self.__objects = {
                    key: classes[key.split('.')[0]](**obj)
                    for key, obj in _dict.items()
                }
        except FileNotFoundError:
            pass
