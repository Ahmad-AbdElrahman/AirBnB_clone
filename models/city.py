#!usr/bin/python3
from .base_model import BaseModel


class City(BaseModel):
    name = ""
    state_id = ""  # it will be the State.id later
