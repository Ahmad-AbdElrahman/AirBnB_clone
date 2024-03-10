#!/usr/bin/python3
"""Defines unittests for the `file_storage.py` module"""
import os
import models
import unittest
from models import FileStorage
from models import classes


class TestFileStorage_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""

    def test_FileStorage_instantiation_no_args(self):
        """Basic test"""
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        """Basic test"""
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_storage_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    def setUp(self):
        """Init setup for the test"""
        pass

    def tearDown(self) -> None:
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_storage_type(self):
        """Test the storage type"""
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(self):
        """Passing an invalid arg to all() method"""
        with self.assertRaises(TypeError):
            models.storage.all({})

    def test_new(self):
        """Test new() method"""
        bm = classes["BaseModel"]()
        am = classes["Amenity"]()
        rv = classes["Review"]()
        st = classes["State"]()
        pl = classes["Place"]()
        us = classes["User"]()
        cy = classes["City"]()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        self.assertIn("BaseModel." + bm.id, models.storage.all().keys())
        self.assertIn(bm, models.storage.all().values())
        self.assertIn("User." + us.id, models.storage.all().keys())
        self.assertIn(us, models.storage.all().values())
        self.assertIn("State." + st.id, models.storage.all().keys())
        self.assertIn(st, models.storage.all().values())
        self.assertIn("Place." + pl.id, models.storage.all().keys())
        self.assertIn(pl, models.storage.all().values())
        self.assertIn("City." + cy.id, models.storage.all().keys())
        self.assertIn(cy, models.storage.all().values())
        self.assertIn("Amenity." + am.id, models.storage.all().keys())
        self.assertIn(am, models.storage.all().values())
        self.assertIn("Review." + rv.id, models.storage.all().keys())
        self.assertIn(rv, models.storage.all().values())

    def test_new_with_args(self):
        """Test new() method with extra arg"""
        with self.assertRaises(TypeError):
            models.storage.new(classes["BaseModel"](), 1)

    def test_new_with_None(self):
        """Test new() method with arg type None"""
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_save(self):
        """Test save() method"""
        bm = classes["BaseModel"]()
        am = classes["Amenity"]()
        rv = classes["Review"]()
        st = classes["State"]()
        pl = classes["Place"]()
        us = classes["User"]()
        cy = classes["City"]()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        models.storage.save()
        save_text = ""
        with open("hbnb.json", "r") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + bm.id, save_text)
            self.assertIn("User." + us.id, save_text)
            self.assertIn("State." + st.id, save_text)
            self.assertIn("Place." + pl.id, save_text)
            self.assertIn("City." + cy.id, save_text)
            self.assertIn("Amenity." + am.id, save_text)
            self.assertIn("Review." + rv.id, save_text)

    def test_save_with_arg(self):
        """Test save() method with arg"""
        with self.assertRaises(TypeError):
            models.storage.save({})

    def test_reload(self):
        """Test reload() method"""
        bm = classes["BaseModel"]()
        am = classes["Amenity"]()
        rv = classes["Review"]()
        st = classes["State"]()
        pl = classes["Place"]()
        us = classes["User"]()
        cy = classes["City"]()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + bm.id, objs)
        self.assertIn("User." + us.id, objs)
        self.assertIn("State." + st.id, objs)
        self.assertIn("Place." + pl.id, objs)
        self.assertIn("City." + cy.id, objs)
        self.assertIn("Amenity." + am.id, objs)
        self.assertIn("Review." + rv.id, objs)

    def test_reload_with_arg(self):
        """Test reload() method with arg"""
        with self.assertRaises(TypeError):
            models.storage.reload({})


if __name__ == "__main__":
    unittest.main()
