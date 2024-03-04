#!/usr/bin/python3
import json


class FileStorage:
    __file_path = "hbnb.json"
    __objects = {}  # format: <class name>.id ex: BaseModel.123

    def all(self):
        """
        returns the dictionary __objects
        """
        return self.__objects

    def new(self, obj):
        """
        sets in __objects the obj with key <obj class name>.id
        """
        self.__objects[self.__class__.__name__ + '.' + str(obj)] = obj

    def save(self):
        """
        serializes __objects to the JSON file (path: __file_path)
        """
        with open(self.__file_path, 'w') as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f)

    def reload(self):
        """
        deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists; otherwise, do nothing.)
        (If the file doesn't exist, no exception should be raised)
        """
        pass
