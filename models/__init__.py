#!/usr/bin/python3
"""Defines the storage object of the engine module"""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
