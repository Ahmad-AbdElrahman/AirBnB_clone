#!/usr/bin/python3
"""Defines the unittests for the console.py module"""
import os
import json
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBConsole, error_messages
from models import classes, storage


class TestConsoleExitOp(unittest.TestCase):

    def setUp(self):
        self.console = HBNBConsole()

    def test_quit(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("quit")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "")

    def test_EOF(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd("EOF")
        output = mock_stdout.getvalue()
        self.assertEqual(output, "\n")


class TestBaseModel(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.console = HBNBConsole()
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
        obj = list(storage.all().values())[0]
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
        obj = list(storage.all().values())[0]
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} name \"xxx\""
            self.console.onecmd(cmd)
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "xxx")

    def test_update_with_extra_attrs(self):
        obj = list(storage.all().values())[0]
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} age \"20\" color \"red\""
            self.console.onecmd(cmd)
        self.assertIn("age", obj.__dict__.keys())
        self.assertNotIn("color", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")

    def test_update_with_dict(self):
        obj = list(storage.all().values())[0]
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
        obj = list(storage.all().values())[0]
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} {obj.id}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        obj = list(storage.all().values())[0]
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"update {self.cls_name} {obj.id} color")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_val"]
        self.assertEqual(output, expected)

    def test_do_count(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.console.onecmd(f"count {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "1")

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

    # THIS z 👇 IS IMPORTANT
    def test_z_destroy(self):
        obj = list(storage.all().values())[0]
        with patch('sys.stdout', new=StringIO()):
            self.console.onecmd(f"destroy {self.cls_name} {obj.id}")
        self.assertNotIn(f"{self.cls_name}.{obj.id}", storage.all().keys())


# class TestUser(unittest.TestCase):

#     @classmethod
#     def setUp(cls):
#         cls.console = HBNBConsole()
#         cls.cls_name = "User"

#     @classmethod
#     def tearDown(cls):
#         if os.path.exists(cls.console.file):
#             os.remove(cls.console.file)

#     def test_create(self):
#         """Test the create method using the <method> <class> formate."""
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd(f"create {self.cls_name}")
#         output = mock_stdout.getvalue().strip()
#         self.assertIsInstance(output, str)
#         uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
#         self.assertRegex(output, uuid_pattern)
#         self.assertIn(f"{self.cls_name}.{output}", storage.all().keys())

#     def test_create_without_clsname(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd("create")
#         output = mock_stdout.getvalue().strip()
#         expected = error_messages["no_cls_name"]
#         self.assertEqual(output, expected)

#     def test_create_with_invalid_clsname(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd("create base")
#         output = mock_stdout.getvalue().strip()
#         expected = error_messages["no_cls"]
#         self.assertEqual(output, expected)

#     def test_show(self):
#         obj = list(storage.all().values())[0]
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd(f"show {self.cls_name} {obj.id}")
#             output = mock_stdout.getvalue().strip()
#         self.assertEqual(output, obj.__str__())

#     def test_show_without_clsname(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd("show")
#         output = mock_stdout.getvalue().strip()
#         expected = error_messages["no_cls_name"]
#         self.assertEqual(output, expected)

#     def test_show_with_invalid_clsname(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd("show base")
#         output = mock_stdout.getvalue().strip()
#         expected = error_messages["no_cls"]
#         self.assertEqual(output, expected)

#     def test_show_with_invalid_id(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd(f"show {self.cls_name} 123")
#         output = mock_stdout.getvalue().strip()
#         expected = error_messages["no_obj"]
#         self.assertEqual(output, expected)

#     def test_update(self):
#         obj = list(storage.all().values())[0]
#         with patch('sys.stdout', new=StringIO()):
#             cmd = f"update {self.cls_name} {obj.id} name \"xxx\""
#             self.console.onecmd(cmd)
#         self.assertIn("name", obj.__dict__.keys())
#         self.assertEqual(obj.__dict__["name"], "xxx")

#     def test_update_with_extra_attrs(self):
#         obj = list(storage.all().values())[0]
#         with patch('sys.stdout', new=StringIO()):
#             cmd = f"update {self.cls_name} {obj.id} age \"20\" color \"red\""
#             self.console.onecmd(cmd)
#         self.assertIn("age", obj.__dict__.keys())
#         self.assertNotIn("color", obj.__dict__.keys())
#         self.assertEqual(obj.__dict__["age"], "20")

#     def test_update_with_dict(self):
#         obj = list(storage.all().values())[0]
#         with patch('sys.stdout', new=StringIO()):
#             cmd = f"update {self.cls_name} {obj.id} {{\"email\": \"xxx@gm\"}}"
#             self.console.onecmd(cmd)
#         self.assertIn("email", obj.__dict__.keys())
#         self.assertEqual(obj.__dict__["email"], "xxx@gm")

#     def test_update_without_clsname(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd(f"update")
#         output = mock_stdout.getvalue().strip()
#         expected = error_messages["no_cls_name"]
#         self.assertEqual(output, expected)

#     def test_update_with_invalid_clsname(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd(f"update base")
#         output = mock_stdout.getvalue().strip()
#         expected = error_messages["no_cls"]
#         self.assertEqual(output, expected)

#     def test_update_without_id(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd(f"update {self.cls_name}")
#         output = mock_stdout.getvalue().strip()
#         expected = error_messages["no_obj_id"]
#         self.assertEqual(output, expected)

#     def test_update_with_invalid_id(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd(f"update {self.cls_name} 123 age 20")
#         output = mock_stdout.getvalue().strip()
#         expected = error_messages["no_obj"]
#         self.assertEqual(output, expected)

#     def test_update_without_attrname(self):
#         obj = list(storage.all().values())[0]
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd(f"update {self.cls_name} {obj.id}")
#         output = mock_stdout.getvalue().strip()
#         expected = error_messages["no_attr_name"]
#         self.assertEqual(output, expected)

#     def test_update_without_attrvalue(self):
#         obj = list(storage.all().values())[0]
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd(f"update {self.cls_name} {obj.id} color")
#         output = mock_stdout.getvalue().strip()
#         expected = error_messages["no_attr_val"]
#         self.assertEqual(output, expected)

#     def test_do_count(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd(f"count {self.cls_name}")
#         output = mock_stdout.getvalue().strip()
#         self.assertEqual(output, "1")

#     def test_destroy_without_clsname(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd(f"destroy")
#         output = mock_stdout.getvalue().strip()
#         expected = error_messages["no_cls_name"]
#         self.assertEqual(output, expected)

#     def test_destroy_with_invalid_clsname(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd(f"destroy base")
#         output = mock_stdout.getvalue().strip()
#         expected = error_messages["no_cls"]
#         self.assertEqual(output, expected)

#     def test_destroy_without_id(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd(f"destroy {self.cls_name}")
#         output = mock_stdout.getvalue().strip()
#         expected = error_messages["no_obj_id"]
#         self.assertEqual(output, expected)

#     def test_destroy_with_invalid_id(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd(f"destroy {self.cls_name} 123")
#         output = mock_stdout.getvalue().strip()
#         expected = error_messages["no_obj"]
#         self.assertEqual(output, expected)

#     # THIS z 👇 IS IMPORTANT
#     def test_z_destroy(self):
#         obj = list(storage.all().values())[0]
#         with patch('sys.stdout', new=StringIO()):
#             self.console.onecmd(f"destroy {self.cls_name} {obj.id}")
#         self.assertNotIn(f"{self.cls_name}.{obj.id}", storage.all().keys())


# class TestBaseModelDotNotation(unittest.TestCase):

#     @classmethod
#     def setUp(cls):
#         cls.console = HBNBConsole()
#         cls.cls_name = "BaseModel"

#     @classmethod
#     def tearDown(cls):
#
#         if os.path.exists(cls.console.file):
#             os.remove(cls.console.file)

#     def test_create(self):
#         """Test the create method using the <class>.<method>() formate."""
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd(f"{self.cls_name}.create()")
#         output = mock_stdout.getvalue()
#         uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
#         self.assertRegex(output, uuid_pattern)
#         self.assertIn(f"{self.cls_name}.{output}", storage.all().keys())

#     def test_create_with_invalid_clsname(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd("base.create()")
#         output = mock_stdout.getvalue().strip()
#         expected = error_messages["no_cls"]
#         self.assertEqual(output, expected)

#     def test_show(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             bm = classes[self.cls_name]()
#             self.console.onecmd(f"{self.cls_name}.show({bm.id})")
#             result = bm.__str__()
#         output = mock_stdout.getvalue().strip()
#         self.assertEqual(output, result)

#     def test_show_with_invalid_clsname(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd("base.show()")
#         output = mock_stdout.getvalue().strip()
#         expected = error_messages["no_cls"]
#         self.assertEqual(output, expected)

#     def test_show_without_id(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd(f"{self.cls_name}.show()")
#         output = mock_stdout.getvalue().strip()
#         expected = error_messages["no_obj_id"]
#         self.assertEqual(output, expected)

#     def test_show_with_invalid_id(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd(f"{self.cls_name}.show(123)")
#         output = mock_stdout.getvalue().strip()
#         expected = error_messages["no_obj"]
#         self.assertEqual(output, expected)


# class TestConsoleAll(unittest.TestCase):

#     @classmethod
#     def setUp(cls):
#         cls.console = HBNBConsole()

#     @classmethod
#     def tearDown(cls):
#
#         if os.path.exists(cls.console.file):
#             os.remove(cls.console.file)

#     def test_all_is_empty(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd("all")
#         output = mock_stdout.getvalue().strip()
#         self.assertEqual(output, "[]")

#     def test_with_invalid_clsname(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd("all base")
#         output = mock_stdout.getvalue().strip()
#         expected = error_messages["no_cls"]
#         self.assertEqual(output, expected)

#     def test_with_multiple_models(self):
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd("create BaseModel")
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd("create User")
#         with patch('sys.stdout', new=StringIO()) as mock_stdout:
#             self.console.onecmd("all")
#         output = json.loads(mock_stdout.getvalue())
#         self.assertEqual(output[0].split()[0], '[BaseModel]')
#         self.assertEqual(output[1].split()[0], '[User]')


class TestConsoleHelp(unittest.TestCase):

    def test_all(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBConsole().onecmd("help all")
        output = mock_stdout.getvalue().strip().split(".")[0]
        self.assertEqual(
            output,
            "Prints a string representation of all instances",
        )

    def test_quit(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBConsole().onecmd("help quit")
        output = mock_stdout.getvalue().strip().split(".")[0]
        self.assertEqual(
            output,
            "Close the AirBnB console, and exit the program",
        )


if __name__ == "__main__":
    unittest.main()
