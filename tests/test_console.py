#!/usr/bin/python3
"""Defines the unittests for the console.py module"""
import os
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBConsole, classes, error_messages


class TestConsoleExitOP(unittest.TestCase):

    def setUp(self):
        self.console = HBNBConsole()

    def test_quit(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd("quit")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "Quit")

    def test_EOF(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd("EOF")
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "EOF")


class TestConsoleCreateOP(unittest.TestCase):

    def setUp(self):
        self.console = HBNBConsole()

    def tearDown(self):
        if os.path.exists(self.console.file):
            os.remove(self.console.file)

    def test_valid_create_cls(self):
        """Test the create method using the <method> <class> formate."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd("create User")
        output = mock_stdout.getvalue()
        uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
        self.assertRegex(output, uuid_pattern)

    def test_without_cls(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd("create")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls_name"]
        self.assertEqual(output, expected)

    def test_invalid_cls(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd("create user")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)

    def test_valid_cls_create(self):
        """Test the create method using the <class>.<method>() formate."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd("User.create()")
        output = mock_stdout.getvalue()
        uuid_pattern = r"^[a-f0-9]{8}(-[a-f0-9]{4}){3}-[a-f0-9]{12}$"
        self.assertRegex(output, uuid_pattern)

    def test_invalid_cls_create(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd("user.create()")
        output = mock_stdout.getvalue().strip()
        expected = error_messages["no_cls"]
        self.assertEqual(output, expected)


class TestConsoleShowOP(unittest.TestCase):
    def test_do_show(self):
        # Implement test cases for do_show
        pass

    def test_do_all(self):
        # Implement test cases for do_all
        pass

    def test_do_update(self):
        # Implement test cases for do_update
        pass

    def test_do_destroy(self):
        # Implement test cases for do_destroy
        pass

    def test_do_count(self):
        # Implement test cases for do_count
        pass

    def test_validate(self):
        # Implement test cases for the validate function
        pass


if __name__ == "__main__":
    unittest.main()
