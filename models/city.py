#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel


class City(BaseModel):
    name = ""
    state_id = ""  # it will be the State.id later


c = City()
print(c)
