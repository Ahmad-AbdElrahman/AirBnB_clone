#!/usr/bin/python3
"""Defines the storage object of the engine module"""
from models.engine.file_storage import FileStorage
from models.engine.file_storage import classes

storage = FileStorage()
storage.reload()
