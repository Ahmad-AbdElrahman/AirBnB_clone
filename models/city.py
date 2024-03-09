#!/usr/bin/python3
"""Define the City class module"""
from models.base_model import BaseModel


class City(BaseModel):
    name = ""
    state_id = ""  # it will be the State.id later
