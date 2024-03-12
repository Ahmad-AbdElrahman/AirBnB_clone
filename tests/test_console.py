#!/usr/bin/python3
"""Defines the unittests for the console.py module"""
import os
import json
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand, error_messages
from models import classes, storage


class TestConsoleExitOp(unittest.TestCase):
    """Testing the exit methods of the console."""

    def test_quit(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd("quit")
        output = mock_stdout.getvalue()
        self.assertEqual(output, "")

    def test_EOF(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd("EOF")
        output = mock_stdout.getvalue()
        self.assertEqual(output, "\n")


class TestBaseModel(unittest.TestCase):
    """Testing the BaseModel"""

    @classmethod
    def setUp(cls):
        cls.console = HBNBCommand()
        cls.cls_name = "BaseModel"

    @classmethod
    def tearDown(cls):
        if os.path.exists(cls.console.file):
            os.remove(cls.console.file)

    def test_create(self):
        """Test the create method using the <method> <class> formate."""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"create {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        self.assertIsInstance(output, str)
        uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
        self.assertRegex(output, uuid_pattern)
        self.assertIn(f"{self.cls_name}.{output}", storage.all().keys())

    def test_create_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("create")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_create_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("create base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"show {self.cls_name} {obj.id}")
            output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("show")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("show base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"show {self.cls_name} 123")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} name \"xxx\""
            self.console.onecmd(cmd)
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "xxx")

    def test_update_with_extra_attrs(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} age \"20\" color \"red\""
            self.console.onecmd(cmd)
        self.assertIn("age", obj.__dict__.keys())
        self.assertNotIn("color", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")

    def test_update_with_dict(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} {{\"email\": \"xxx@gm\"}}"
            self.console.onecmd(cmd)
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "xxx@gm")

    def test_update_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} 123 age 20")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} {obj.id}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} {obj.id} color")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_val"]
        self.assertEqual(output, expected)

    def test_do_count(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"count {self.cls_name}")
        output = mock_stdout.getvalue()
        count = 0
        for i in storage.all().values():
            if type(i) == classes[self.cls_name]:
                count += 1
        self.assertEqual(int(output), count)

    def test_destroy(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            self.console.onecmd(f"destroy {self.cls_name} {obj.id}")
        self.assertNotIn(f"{self.cls_name}.{obj.id}", storage.all().keys())

    def test_destroy_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy {self.cls_name} 123")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)


class TestBaseModelDotNotation(unittest.TestCase):
    """Testing with the method.notation formate"""

    @classmethod
    def setUp(cls):
        cls.console = HBNBCommand()
        cls.cls_name = "BaseModel"

    @classmethod
    def tearDown(cls):
        if os.path.exists(cls.console.file):
            os.remove(cls.console.file)

    # def test_create(self):
    #     """Test the create method using the <class>.<method>() formate."""
    #     with patch('sys.stdout', new=StringIO()) as mock_stdout:
    #         self.console.default(f"{self.cls_name}.create()")
    #     output = mock_stdout.getvalue().strip()
    #     uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
    #     self.assertRegex(output, uuid_pattern)
    #     self.assertIn(f"{self.cls_name}.{output}", storage.all().keys())

    # def test_create_with_invalid_clsname(self):
    #     with patch('sys.stdout', new=StringIO()) as mock_stdout:
    #         self.console.default("base.create()")
    #     output = mock_stdout.getvalue().strip()
    #     expected = error_messages["no_cls"]
    #     self.assertEqual(output, expected)

    def test_show(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.show({obj.id})")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default("base.show()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.show()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.show(123)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, name \"xxx\")"
            self.console.default(cmd)
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "xxx")

    def test_update_with_extra_attrs(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, age \"20\", color \"red\")"
            self.console.default(cmd)
        self.assertIn("age", obj.__dict__.keys())
        self.assertNotIn("color", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")

    def test_update_with_dict(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, {{\"email\": \"xxx@gm\"}})"
            self.console.default(cmd)
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "xxx@gm")

    def test_update_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"base.update()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update(123, age 20)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update({obj.id})")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update({obj.id}, age)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_val"]
        self.assertEqual(output, expected)

    def test_do_count(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.count()")
        output = mock_stdout.getvalue()
        count = 0
        for i in storage.all().values():
            if type(i) == classes[self.cls_name]:
                count += 1
        self.assertEqual(int(output), count)

    def test_destroy(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            self.console.default(f"{self.cls_name}.destroy({obj.id})")
        self.assertNotIn(f"{self.cls_name}.{obj.id}", storage.all().keys())

    def test_destroy_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"base.destroy()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.destroy()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.destroy(123)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)


class TestUser(unittest.TestCase):
    """Testing the User Model"""

    @classmethod
    def setUp(cls):
        cls.console = HBNBCommand()
        cls.cls_name = "User"

    @classmethod
    def tearDown(cls):
        if os.path.exists(cls.console.file):
            os.remove(cls.console.file)

    def test_create(self):
        """Test the create method using the <method> <class> formate."""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"create {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        self.assertIsInstance(output, str)
        uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
        self.assertRegex(output, uuid_pattern)
        self.assertIn(f"{self.cls_name}.{output}", storage.all().keys())

    def test_create_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("create")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_create_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("create base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"show {self.cls_name} {obj.id}")
            output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("show")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("show base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"show {self.cls_name} 123")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} name \"xxx\""
            self.console.onecmd(cmd)
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "xxx")

    def test_update_with_extra_attrs(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} age \"20\" color \"red\""
            self.console.onecmd(cmd)
        self.assertIn("age", obj.__dict__.keys())
        self.assertNotIn("color", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")

    def test_update_with_dict(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} {{\"email\": \"xxx@gm\"}}"
            self.console.onecmd(cmd)
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "xxx@gm")

    def test_update_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} 123 age 20")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} {obj.id}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} {obj.id} color")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_val"]
        self.assertEqual(output, expected)

    def test_count(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"count {self.cls_name}")
        output = mock_stdout.getvalue()
        count = 0
        for i in storage.all().values():
            if type(i) == classes[self.cls_name]:
                count += 1
        self.assertEqual(int(output), count)

    def test_destroy(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            self.console.onecmd(f"destroy {self.cls_name} {obj.id}")
        self.assertNotIn(f"{self.cls_name}.{obj.id}", storage.all().keys())

    def test_destroy_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy {self.cls_name} 123")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)


class TestUserDotNotation(unittest.TestCase):
    """Testing with the method.notation formate"""

    @classmethod
    def setUp(cls):
        cls.console = HBNBCommand()
        cls.cls_name = "User"

    @classmethod
    def tearDown(cls):
        if os.path.exists(cls.console.file):
            os.remove(cls.console.file)

    # def test_create(self):
    #     """Test the create method using the <class>.<method>() formate."""
    #     with patch('sys.stdout', new=StringIO()) as mock_stdout:
    #         self.console.default(f"{self.cls_name}.create()")
    #     output = mock_stdout.getvalue().strip()
    #     uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
    #     self.assertRegex(output, uuid_pattern)
    #     self.assertIn(f"{self.cls_name}.{output}", storage.all().keys())

    # def test_create_with_invalid_clsname(self):
    #     with patch('sys.stdout', new=StringIO()) as mock_stdout:
    #         self.console.default("base.create()")
    #     output = mock_stdout.getvalue().strip()
    #     expected = error_messages["no_cls"]
    #     self.assertEqual(output, expected)

    def test_show(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.show({obj.id})")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default("base.show()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.show()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.show(123)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, name \"xxx\")"
            self.console.default(cmd)
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "xxx")

    def test_update_with_extra_attrs(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, age \"20\", color \"red\")"
            self.console.default(cmd)
        self.assertIn("age", obj.__dict__.keys())
        self.assertNotIn("color", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")

    def test_update_with_dict(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, {{\"email\": \"xxx@gm\"}})"
            self.console.default(cmd)
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "xxx@gm")

    def test_update_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"base.update()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update(123, age 20)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update({obj.id})")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update({obj.id}, age)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_val"]
        self.assertEqual(output, expected)

    def test_do_count(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.count()")
        output = mock_stdout.getvalue()
        count = 0
        for i in storage.all().values():
            if type(i) == classes[self.cls_name]:
                count += 1
        self.assertEqual(int(output), count)

    def test_destroy(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            self.console.default(f"{self.cls_name}.destroy({obj.id})")
        self.assertNotIn(f"{self.cls_name}.{obj.id}", storage.all().keys())

    def test_destroy_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"base.destroy()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.destroy()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.destroy(123)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)


class TestState(unittest.TestCase):
    """Testing the State Model"""

    @classmethod
    def setUp(cls):
        cls.console = HBNBCommand()
        cls.cls_name = "State"

    @classmethod
    def tearDown(cls):
        if os.path.exists(cls.console.file):
            os.remove(cls.console.file)

    def test_create(self):
        """Test the create method using the <method> <class> formate."""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"create {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        self.assertIsInstance(output, str)
        uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
        self.assertRegex(output, uuid_pattern)
        self.assertIn(f"{self.cls_name}.{output}", storage.all().keys())

    def test_create_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("create")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_create_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("create base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"show {self.cls_name} {obj.id}")
            output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("show")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("show base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"show {self.cls_name} 123")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} name \"xxx\""
            self.console.onecmd(cmd)
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "xxx")

    def test_update_with_extra_attrs(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} age \"20\" color \"red\""
            self.console.onecmd(cmd)
        self.assertIn("age", obj.__dict__.keys())
        self.assertNotIn("color", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")

    def test_update_with_dict(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} {{\"email\": \"xxx@gm\"}}"
            self.console.onecmd(cmd)
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "xxx@gm")

    def test_update_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} 123 age 20")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} {obj.id}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} {obj.id} color")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_val"]
        self.assertEqual(output, expected)

    def test_count(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"count {self.cls_name}")
        output = mock_stdout.getvalue()
        count = 0
        for i in storage.all().values():
            if type(i) == classes[self.cls_name]:
                count += 1
        self.assertEqual(int(output), count)

    def test_destroy(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            self.console.onecmd(f"destroy {self.cls_name} {obj.id}")
        self.assertNotIn(f"{self.cls_name}.{obj.id}", storage.all().keys())

    def test_destroy_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy {self.cls_name} 123")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)


class TestStateDotNotation(unittest.TestCase):
    """Testing with the method.notation formate"""

    @classmethod
    def setUp(cls):
        cls.console = HBNBCommand()
        cls.cls_name = "State"

    @classmethod
    def tearDown(cls):
        if os.path.exists(cls.console.file):
            os.remove(cls.console.file)

    # def test_create(self):
    #     """Test the create method using the <class>.<method>() formate."""
    #     with patch('sys.stdout', new=StringIO()) as mock_stdout:
    #         self.console.default(f"{self.cls_name}.create()")
    #     output = mock_stdout.getvalue().strip()
    #     uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
    #     self.assertRegex(output, uuid_pattern)
    #     self.assertIn(f"{self.cls_name}.{output}", storage.all().keys())

    # def test_create_with_invalid_clsname(self):
    #     with patch('sys.stdout', new=StringIO()) as mock_stdout:
    #         self.console.default("base.create()")
    #     output = mock_stdout.getvalue().strip()
    #     expected = error_messages["no_cls"]
    #     self.assertEqual(output, expected)

    def test_show(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.show({obj.id})")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default("base.show()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.show()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.show(123)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, name \"xxx\")"
            self.console.default(cmd)
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "xxx")

    def test_update_with_extra_attrs(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, age \"20\", color \"red\")"
            self.console.default(cmd)
        self.assertIn("age", obj.__dict__.keys())
        self.assertNotIn("color", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")

    def test_update_with_dict(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, {{\"email\": \"xxx@gm\"}})"
            self.console.default(cmd)
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "xxx@gm")

    def test_update_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"base.update()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update(123, age 20)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update({obj.id})")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update({obj.id}, age)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_val"]
        self.assertEqual(output, expected)

    def test_do_count(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.count()")
        output = mock_stdout.getvalue()
        count = 0
        for i in storage.all().values():
            if type(i) == classes[self.cls_name]:
                count += 1
        self.assertEqual(int(output), count)

    def test_destroy(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            self.console.default(f"{self.cls_name}.destroy({obj.id})")
        self.assertNotIn(f"{self.cls_name}.{obj.id}", storage.all().keys())

    def test_destroy_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"base.destroy()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.destroy()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.destroy(123)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)


class TestReview(unittest.TestCase):
    """Testing the Review Model"""

    @classmethod
    def setUp(cls):
        cls.console = HBNBCommand()
        cls.cls_name = "Review"

    @classmethod
    def tearDown(cls):
        if os.path.exists(cls.console.file):
            os.remove(cls.console.file)

    def test_create(self):
        """Test the create method using the <method> <class> formate."""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"create {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        self.assertIsInstance(output, str)
        uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
        self.assertRegex(output, uuid_pattern)
        self.assertIn(f"{self.cls_name}.{output}", storage.all().keys())

    def test_create_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("create")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_create_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("create base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"show {self.cls_name} {obj.id}")
            output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("show")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("show base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"show {self.cls_name} 123")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} name \"xxx\""
            self.console.onecmd(cmd)
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "xxx")

    def test_update_with_extra_attrs(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} age \"20\" color \"red\""
            self.console.onecmd(cmd)
        self.assertIn("age", obj.__dict__.keys())
        self.assertNotIn("color", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")

    def test_update_with_dict(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} {{\"email\": \"xxx@gm\"}}"
            self.console.onecmd(cmd)
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "xxx@gm")

    def test_update_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} 123 age 20")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} {obj.id}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} {obj.id} color")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_val"]
        self.assertEqual(output, expected)

    def test_count(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"count {self.cls_name}")
        output = mock_stdout.getvalue()
        count = 0
        for i in storage.all().values():
            if type(i) == classes[self.cls_name]:
                count += 1
        self.assertEqual(int(output), count)

    def test_destroy(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            self.console.onecmd(f"destroy {self.cls_name} {obj.id}")
        self.assertNotIn(f"{self.cls_name}.{obj.id}", storage.all().keys())

    def test_destroy_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy {self.cls_name} 123")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)


class TestReviewDotNotation(unittest.TestCase):
    """Testing with the method.notation formate"""

    @classmethod
    def setUp(cls):
        cls.console = HBNBCommand()
        cls.cls_name = "Review"

    @classmethod
    def tearDown(cls):
        if os.path.exists(cls.console.file):
            os.remove(cls.console.file)

    # def test_create(self):
    #     """Test the create method using the <class>.<method>() formate."""
    #     with patch('sys.stdout', new=StringIO()) as mock_stdout:
    #         self.console.default(f"{self.cls_name}.create()")
    #     output = mock_stdout.getvalue().strip()
    #     uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
    #     self.assertRegex(output, uuid_pattern)
    #     self.assertIn(f"{self.cls_name}.{output}", storage.all().keys())

    # def test_create_with_invalid_clsname(self):
    #     with patch('sys.stdout', new=StringIO()) as mock_stdout:
    #         self.console.default("base.create()")
    #     output = mock_stdout.getvalue().strip()
    #     expected = error_messages["no_cls"]
    #     self.assertEqual(output, expected)

    def test_show(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.show({obj.id})")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default("base.show()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.show()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.show(123)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, name \"xxx\")"
            self.console.default(cmd)
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "xxx")

    def test_update_with_extra_attrs(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, age \"20\", color \"red\")"
            self.console.default(cmd)
        self.assertIn("age", obj.__dict__.keys())
        self.assertNotIn("color", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")

    def test_update_with_dict(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, {{\"email\": \"xxx@gm\"}})"
            self.console.default(cmd)
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "xxx@gm")

    def test_update_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"base.update()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update(123, age 20)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update({obj.id})")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update({obj.id}, age)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_val"]
        self.assertEqual(output, expected)

    def test_do_count(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.count()")
        output = mock_stdout.getvalue()
        count = 0
        for i in storage.all().values():
            if type(i) == classes[self.cls_name]:
                count += 1
        self.assertEqual(int(output), count)

    def test_destroy(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            self.console.default(f"{self.cls_name}.destroy({obj.id})")
        self.assertNotIn(f"{self.cls_name}.{obj.id}", storage.all().keys())

    def test_destroy_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"base.destroy()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.destroy()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.destroy(123)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)


class TestPlace(unittest.TestCase):
    """Testing the Place Model"""

    @classmethod
    def setUp(cls):
        cls.console = HBNBCommand()
        cls.cls_name = "Place"

    @classmethod
    def tearDown(cls):
        if os.path.exists(cls.console.file):
            os.remove(cls.console.file)

    def test_create(self):
        """Test the create method using the <method> <class> formate."""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"create {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        self.assertIsInstance(output, str)
        uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
        self.assertRegex(output, uuid_pattern)
        self.assertIn(f"{self.cls_name}.{output}", storage.all().keys())

    def test_create_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("create")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_create_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("create base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"show {self.cls_name} {obj.id}")
            output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("show")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("show base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"show {self.cls_name} 123")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} name \"xxx\""
            self.console.onecmd(cmd)
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "xxx")

    def test_update_with_extra_attrs(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} age \"20\" color \"red\""
            self.console.onecmd(cmd)
        self.assertIn("age", obj.__dict__.keys())
        self.assertNotIn("color", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")

    def test_update_with_dict(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} {{\"email\": \"xxx@gm\"}}"
            self.console.onecmd(cmd)
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "xxx@gm")

    def test_update_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} 123 age 20")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} {obj.id}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} {obj.id} color")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_val"]
        self.assertEqual(output, expected)

    def test_count(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"count {self.cls_name}")
        output = mock_stdout.getvalue()
        count = 0
        for i in storage.all().values():
            if type(i) == classes[self.cls_name]:
                count += 1
        self.assertEqual(int(output), count)

    def test_destroy(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            self.console.onecmd(f"destroy {self.cls_name} {obj.id}")
        self.assertNotIn(f"{self.cls_name}.{obj.id}", storage.all().keys())

    def test_destroy_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy {self.cls_name} 123")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)


class TestPlaceDotNotation(unittest.TestCase):
    """Testing with the method.notation formate"""

    @classmethod
    def setUp(cls):
        cls.console = HBNBCommand()
        cls.cls_name = "Place"

    @classmethod
    def tearDown(cls):
        if os.path.exists(cls.console.file):
            os.remove(cls.console.file)

    # def test_create(self):
    #     """Test the create method using the <class>.<method>() formate."""
    #     with patch('sys.stdout', new=StringIO()) as mock_stdout:
    #         self.console.default(f"{self.cls_name}.create()")
    #     output = mock_stdout.getvalue().strip()
    #     uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
    #     self.assertRegex(output, uuid_pattern)
    #     self.assertIn(f"{self.cls_name}.{output}", storage.all().keys())

    # def test_create_with_invalid_clsname(self):
    #     with patch('sys.stdout', new=StringIO()) as mock_stdout:
    #         self.console.default("base.create()")
    #     output = mock_stdout.getvalue().strip()
    #     expected = error_messages["no_cls"]
    #     self.assertEqual(output, expected)

    def test_show(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.show({obj.id})")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default("base.show()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.show()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.show(123)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, name \"xxx\")"
            self.console.default(cmd)
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "xxx")

    def test_update_with_extra_attrs(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, age \"20\", color \"red\")"
            self.console.default(cmd)
        self.assertIn("age", obj.__dict__.keys())
        self.assertNotIn("color", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")

    def test_update_with_dict(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, {{\"email\": \"xxx@gm\"}})"
            self.console.default(cmd)
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "xxx@gm")

    def test_update_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"base.update()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update(123, age 20)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update({obj.id})")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update({obj.id}, age)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_val"]
        self.assertEqual(output, expected)

    def test_do_count(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.count()")
        output = mock_stdout.getvalue()
        count = 0
        for i in storage.all().values():
            if type(i) == classes[self.cls_name]:
                count += 1
        self.assertEqual(int(output), count)

    def test_destroy(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            self.console.default(f"{self.cls_name}.destroy({obj.id})")
        self.assertNotIn(f"{self.cls_name}.{obj.id}", storage.all().keys())

    def test_destroy_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"base.destroy()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.destroy()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.destroy(123)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)


class TestCity(unittest.TestCase):
    """Testing the City Model"""

    @classmethod
    def setUp(cls):
        cls.console = HBNBCommand()
        cls.cls_name = "City"

    @classmethod
    def tearDown(cls):
        if os.path.exists(cls.console.file):
            os.remove(cls.console.file)

    def test_create(self):
        """Test the create method using the <method> <class> formate."""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"create {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        self.assertIsInstance(output, str)
        uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
        self.assertRegex(output, uuid_pattern)
        self.assertIn(f"{self.cls_name}.{output}", storage.all().keys())

    def test_create_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("create")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_create_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("create base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"show {self.cls_name} {obj.id}")
            output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("show")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("show base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"show {self.cls_name} 123")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} name \"xxx\""
            self.console.onecmd(cmd)
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "xxx")

    def test_update_with_extra_attrs(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} age \"20\" color \"red\""
            self.console.onecmd(cmd)
        self.assertIn("age", obj.__dict__.keys())
        self.assertNotIn("color", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")

    def test_update_with_dict(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} {{\"email\": \"xxx@gm\"}}"
            self.console.onecmd(cmd)
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "xxx@gm")

    def test_update_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} 123 age 20")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} {obj.id}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} {obj.id} color")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_val"]
        self.assertEqual(output, expected)

    def test_count(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"count {self.cls_name}")
        output = mock_stdout.getvalue()
        count = 0
        for i in storage.all().values():
            if type(i) == classes[self.cls_name]:
                count += 1
        self.assertEqual(int(output), count)

    def test_destroy(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            self.console.onecmd(f"destroy {self.cls_name} {obj.id}")
        self.assertNotIn(f"{self.cls_name}.{obj.id}", storage.all().keys())

    def test_destroy_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy {self.cls_name} 123")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)


class TestCityDotNotation(unittest.TestCase):
    """Testing with the method.notation formate"""

    @classmethod
    def setUp(cls):
        cls.console = HBNBCommand()
        cls.cls_name = "City"

    @classmethod
    def tearDown(cls):
        if os.path.exists(cls.console.file):
            os.remove(cls.console.file)

    # def test_create(self):
    #     """Test the create method using the <class>.<method>() formate."""
    #     with patch('sys.stdout', new=StringIO()) as mock_stdout:
    #         self.console.default(f"{self.cls_name}.create()")
    #     output = mock_stdout.getvalue().strip()
    #     uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
    #     self.assertRegex(output, uuid_pattern)
    #     self.assertIn(f"{self.cls_name}.{output}", storage.all().keys())

    # def test_create_with_invalid_clsname(self):
    #     with patch('sys.stdout', new=StringIO()) as mock_stdout:
    #         self.console.default("base.create()")
    #     output = mock_stdout.getvalue().strip()
    #     expected = error_messages["no_cls"]
    #     self.assertEqual(output, expected)

    def test_show(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.show({obj.id})")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default("base.show()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.show()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.show(123)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, name \"xxx\")"
            self.console.default(cmd)
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "xxx")

    def test_update_with_extra_attrs(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, age \"20\", color \"red\")"
            self.console.default(cmd)
        self.assertIn("age", obj.__dict__.keys())
        self.assertNotIn("color", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")

    def test_update_with_dict(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, {{\"email\": \"xxx@gm\"}})"
            self.console.default(cmd)
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "xxx@gm")

    def test_update_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"base.update()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update(123, age 20)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update({obj.id})")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update({obj.id}, age)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_val"]
        self.assertEqual(output, expected)

    def test_do_count(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.count()")
        output = mock_stdout.getvalue()
        count = 0
        for i in storage.all().values():
            if type(i) == classes[self.cls_name]:
                count += 1
        self.assertEqual(int(output), count)

    def test_destroy(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            self.console.default(f"{self.cls_name}.destroy({obj.id})")
        self.assertNotIn(f"{self.cls_name}.{obj.id}", storage.all().keys())

    def test_destroy_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"base.destroy()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.destroy()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.destroy(123)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)


class TestAmenity(unittest.TestCase):
    """Testing the Amenity Model"""

    @classmethod
    def setUp(cls):
        cls.console = HBNBCommand()
        cls.cls_name = "Amenity"

    @classmethod
    def tearDown(cls):
        if os.path.exists(cls.console.file):
            os.remove(cls.console.file)

    def test_create(self):
        """Test the create method using the <method> <class> formate."""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"create {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        self.assertIsInstance(output, str)
        uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
        self.assertRegex(output, uuid_pattern)
        self.assertIn(f"{self.cls_name}.{output}", storage.all().keys())

    def test_create_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("create")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_create_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("create base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"show {self.cls_name} {obj.id}")
            output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("show")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("show base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"show {self.cls_name} 123")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} name \"xxx\""
            self.console.onecmd(cmd)
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "xxx")

    def test_update_with_extra_attrs(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} age \"20\" color \"red\""
            self.console.onecmd(cmd)
        self.assertIn("age", obj.__dict__.keys())
        self.assertNotIn("color", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")

    def test_update_with_dict(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} {{\"email\": \"xxx@gm\"}}"
            self.console.onecmd(cmd)
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "xxx@gm")

    def test_update_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} 123 age 20")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} {obj.id}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} {obj.id} color")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_val"]
        self.assertEqual(output, expected)

    def test_count(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"count {self.cls_name}")
        output = mock_stdout.getvalue()
        count = 0
        for i in storage.all().values():
            if type(i) == classes[self.cls_name]:
                count += 1
        self.assertEqual(int(output), count)

    def test_destroy(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            self.console.onecmd(f"destroy {self.cls_name} {obj.id}")
        self.assertNotIn(f"{self.cls_name}.{obj.id}", storage.all().keys())

    def test_destroy_without_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"destroy {self.cls_name} 123")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)


class TestAmenityDotNotation(unittest.TestCase):
    """Testing with the method.notation formate"""

    @classmethod
    def setUp(cls):
        cls.console = HBNBCommand()
        cls.cls_name = "Amenity"

    @classmethod
    def tearDown(cls):
        if os.path.exists(cls.console.file):
            os.remove(cls.console.file)

    # def test_create(self):
    #     """Test the create method using the <class>.<method>() formate."""
    #     with patch('sys.stdout', new=StringIO()) as mock_stdout:
    #         self.console.default(f"{self.cls_name}.create()")
    #     output = mock_stdout.getvalue().strip()
    #     uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
    #     self.assertRegex(output, uuid_pattern)
    #     self.assertIn(f"{self.cls_name}.{output}", storage.all().keys())

    # def test_create_with_invalid_clsname(self):
    #     with patch('sys.stdout', new=StringIO()) as mock_stdout:
    #         self.console.default("base.create()")
    #     output = mock_stdout.getvalue().strip()
    #     expected = error_messages["no_cls"]
    #     self.assertEqual(output, expected)

    def test_show(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.show({obj.id})")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default("base.show()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.show()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.show(123)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, name \"xxx\")"
            self.console.default(cmd)
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "xxx")

    def test_update_with_extra_attrs(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, age \"20\", color \"red\")"
            self.console.default(cmd)
        self.assertIn("age", obj.__dict__.keys())
        self.assertNotIn("color", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")

    def test_update_with_dict(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, {{\"email\": \"xxx@gm\"}})"
            self.console.default(cmd)
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "xxx@gm")

    def test_update_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"base.update()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update(123, age 20)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update({obj.id})")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.update({obj.id}, age)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_val"]
        self.assertEqual(output, expected)

    def test_do_count(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.count()")
        output = mock_stdout.getvalue()
        count = 0
        for i in storage.all().values():
            if type(i) == classes[self.cls_name]:
                count += 1
        self.assertEqual(int(output), count)

    def test_destroy(self):
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            self.console.default(f"{self.cls_name}.destroy({obj.id})")
        self.assertNotIn(f"{self.cls_name}.{obj.id}", storage.all().keys())

    def test_destroy_with_invalid_clsname(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"base.destroy()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.destroy()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.default(f"{self.cls_name}.destroy(123)")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)


if __name__ == "__main__":
    unittest.main()
