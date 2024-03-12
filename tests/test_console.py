#!/usr/bin/python3
"""Defines the unittests for the console.py module"""
import os
import unittest
from io import StringIO
from unittest.mock import patch
from models import storage
from models import classes
from console import HBNBCommand
from console import error_messages


class TestConsoleExitOp(unittest.TestCase):
    """Testing the exit methods of the console."""

    def test_quit(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd("quit")
        output = mock_stdout.getvalue()
        self.assertEqual(output, "")

    def test_EOF(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd("EOF")
        output = mock_stdout.getvalue()
        self.assertEqual(output, "\n")


class TestConsole(unittest.TestCase):
    """
    Testing the console main methods.

    Format:
    -    Like : <method> <class> Ex : create BaseModel
    """

    # @classmethod
    def setUp(self):
        """Initial setup for the class before all operations"""
        self.cls_name = "BaseModel"

    # @classmethod
    def tearDown(self):
        """Tear down setup after all operations"""
        storage._FileStorage__objects = {}
        if os.path.exists(HBNBCommand().file):
            os.remove(HBNBCommand().file)

    def test_create(self):
        """Test the create method"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(f"create {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        self.assertIsInstance(output, str)
        uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
        self.assertRegex(output, uuid_pattern)
        self.assertIn(f"{self.cls_name}.{output}", storage.all().keys())

    def test_create_without_clsname(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd("create")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_create_with_invalid_clsname(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd("create base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show(self):
        """Test"""
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(f"show {self.cls_name} {obj.id}")
            output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_without_clsname(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd("show")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_clsname(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd("show base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(f"show {self.cls_name} 123")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        """Test"""
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} name \"xxx\""
            HBNBCommand().onecmd(cmd)
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "xxx")

    def test_update_with_extra_attrs(self):
        """Test"""
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} age \"20\" color \"red\""
            HBNBCommand().onecmd(cmd)
        self.assertIn("age", obj.__dict__.keys())
        self.assertNotIn("color", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")

    def test_update_with_dict(self):
        """Test"""
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"update {self.cls_name} {obj.id} {{\"email\": \"xxx@gm\"}}"
            HBNBCommand().onecmd(cmd)
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "xxx@gm")

    def test_update_without_clsname(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(f"update")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_clsname(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(f"update base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(f"update {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(f"update {self.cls_name} 123 age 20")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        """Test"""
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(f"update {self.cls_name} {obj.id}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        """Test"""
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(f"update {self.cls_name} {obj.id} color")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_val"]
        self.assertEqual(output, expected)

    def test_do_count(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(f"count {self.cls_name}")
        output = mock_stdout.getvalue()
        count = 0
        for i in storage.all().values():
            if type(i) is classes[self.cls_name]:
                count += 1
        self.assertEqual(int(output), count)

    def test_destroy(self):
        """Test"""
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            HBNBCommand().onecmd(f"destroy {self.cls_name} {obj.id}")
        self.assertNotIn(f"{self.cls_name}.{obj.id}", storage.all().keys())

    def test_destroy_without_clsname(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(f"destroy")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_clsname(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(f"destroy base")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(f"destroy {self.cls_name}")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(f"destroy {self.cls_name} 123")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)


class TestConsoleDotNotation(unittest.TestCase):
    """
    Testing the console main methods using the dot.notation

    Format:
    -    Like : <class>.<method>(). Ex : BaseModel.create()
    """

    # @classmethod
    def setUp(self):
        """Initial setup for the class before all operations"""
        self.cls_name = "BaseModel"

    # @classmethod
    def tearDown(self):
        """Tear down setup after all operations"""
        storage._FileStorage__objects = {}
        if os.path.exists(HBNBCommand().file):
            os.remove(HBNBCommand().file)

    def test_create(self):
        """Test the create method using the <class>.<method>() format."""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"{self.cls_name}.create()")
            )
        output = mock_stdout.getvalue().strip()
        uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
        self.assertRegex(output, uuid_pattern)
        self.assertIn(f"{self.cls_name}.{output}", storage.all().keys())

    def test_create_invalid_clsname(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(HBNBCommand().precmd("base.create()"))
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show(self):
        """Test"""
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"{self.cls_name}.show({obj.id})")
            )
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, obj.__str__())

    def test_show_with_invalid_clsname(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(HBNBCommand().precmd("base.show()"))
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_show_without_id(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"{self.cls_name}.show()")
            )
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_show_with_invalid_id(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"{self.cls_name}.show(123)")
            )
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update(self):
        """Test"""
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            cmd = f"{self.cls_name}.update({obj.id}, name \"xxx\")"
            HBNBCommand().onecmd(HBNBCommand().precmd(cmd))
        self.assertIn("name", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["name"], "xxx")

    def test_update_with_extra_attrs(self):
        """Test"""
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            c = f"{self.cls_name}.update({obj.id}, age \"20\", color \"red\")"
            HBNBCommand().onecmd(HBNBCommand().precmd(c))
        self.assertIn("age", obj.__dict__.keys())
        self.assertNotIn("color", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["age"], "20")

    def test_update_with_dict(self):
        """Test"""
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            c = f"{self.cls_name}.update({obj.id}, {{\"email\": \"xxx@gm\"}})"
            HBNBCommand().onecmd(HBNBCommand().precmd(c))
        self.assertIn("email", obj.__dict__.keys())
        self.assertEqual(obj.__dict__["email"], "xxx@gm")

    def test_update_with_invalid_clsname(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(HBNBCommand().precmd(f"base.update()"))
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_update_without_id(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"{self.cls_name}.update()")
            )
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_update_with_invalid_id(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"{self.cls_name}.update(123, age 20)")
            )
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)

    def test_update_without_attrname(self):
        """Test"""
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"{self.cls_name}.update({obj.id})")
            )
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_name"]
        self.assertEqual(output, expected)

    def test_update_without_attrvalue(self):
        """Test"""
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"{self.cls_name}.update({obj.id}, age)")
            )
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_attr_val"]
        self.assertEqual(output, expected)

    def test_do_count(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"{self.cls_name}.count()")
            )
        output = mock_stdout.getvalue()
        count = 0
        for i in storage.all().values():
            if type(i) is classes[self.cls_name]:
                count += 1
        self.assertEqual(int(output), count)

    def test_destroy(self):
        """Test"""
        obj = classes[self.cls_name]()
        with patch('sys.stdout', new=StringIO()):
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"{self.cls_name}.destroy({obj.id})")
            )
        self.assertNotIn(f"{self.cls_name}.{obj.id}", storage.all().keys())

    def test_destroy_with_invalid_clsname(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(HBNBCommand().precmd(f"base.destroy()"))
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_destroy_without_id(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"{self.cls_name}.destroy()")
            )
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj_id"]
        self.assertEqual(output, expected)

    def test_destroy_with_invalid_id(self):
        """Test"""
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"{self.cls_name}.destroy(123)")
            )
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_obj"]
        self.assertEqual(output, expected)


if __name__ == "__main__":
    unittest.main()
