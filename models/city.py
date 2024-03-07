#!/usr/bin/python3
from models.base_model import BaseModel


class City(BaseModel):
    name = ""
    state_id = ""  # it will be the State.id later


if __name__ == '__main__':
    c = City()
    print(c)
