#!/usr/bin/python3
from .base_model import BaseModel


class Review(BaseModel):
    place_id = ""  # it will be the Place.id later
    user_id = ""  # it will be the User.id later
    text = ""
