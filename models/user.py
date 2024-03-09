#!/usr/bin/python3
"""Define the User class module"""
from models.base_model import BaseModel


class User(BaseModel):

    email = ""
    password = ""
    first_name = ""
    last_name = ""
