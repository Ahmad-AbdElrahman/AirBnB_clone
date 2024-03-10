#!/usr/bin/python3
"""Unit tests for the `city` module"""
import os
import unittest
from datetime import datetime
from models.city import City
from models import FileStorage

c1 = City()
c2 = City(**c1.to_dict())
c3 = City("Giza")


class TestCity(unittest.TestCase):
    """Test cases for the `City` class."""

    def tearDown(self):
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_params(self):
        """Test method for class attributes"""
        self.assertIsInstance(c1.name, str)
        self.assertEqual(c3.name, "")
        c1.name = "Alex"
        self.assertEqual(c1.name, "Alex")

    def test_init(self):
        """Test method for public instances"""
        self.assertIsInstance(c1.id, str)
        self.assertIsInstance(c1.created_at, datetime)
        self.assertIsInstance(c1.updated_at, datetime)
        self.assertEqual(c1.updated_at, c2.updated_at)

    def test_save(self):
        """Test method for save"""
        old_update = c1.updated_at
        c1.save()
        self.assertNotEqual(c1.updated_at, old_update)

    def test_todict(self):
        """Test method for dict"""
        a_dict = c2.to_dict()
        self.assertIsInstance(a_dict, dict)
        self.assertEqual(a_dict['__class__'], type(c2).__name__)
        self.assertIn('created_at', a_dict.keys())
        self.assertIn('updated_at', a_dict.keys())
        self.assertNotEqual(c1, c2)


if __name__ == "__main__":
    unittest.main()
