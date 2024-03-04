#!/usr/bin/python3
from models.base_model import BaseModel
from models.engine import storage

if __name__ == "__main__":
    all_objs = storage.all()
    print("-- Reloaded objects --")
    for obj_id in all_objs.keys():
        obj = all_objs[obj_id]
        print(obj)

    print("-- Create a new object --")
    my_model = BaseModel()
    my_model.name = "My_First_Model"  # type: ignore
    my_model.my_number = 89  # type: ignore
    my_model.save()
    print(my_model)