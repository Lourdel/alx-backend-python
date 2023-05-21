#!/usr/bin/env python3
"""Module defines TestAccessNestedMap"""

import unittest
from typing import Tuple, Dict, Union
from parameterized import parameterized
from unittest.mock import patch, Mock
access_nested_map = __import__("utils").access_nested_map
get_json = __import__("utils").get_json
memoize = __import__("utils").memoize


class TestAccessNestedMap(unittest.TestCase):
    """Class tests Access nested map function"""
    @parameterized.expand(
            [
                ({"a": 1}, ("a",), 1),
                ({"a": {"b": 2}}, ("a",), {"b": 2}),
                ({"a": {"b": 2}}, ("a", "b"), 2)
            ]
        )
    def test_access_nested_map(self, nested_map: Dict, path: Tuple,
                               expected: Union[int, str]):
        """Method tests access_nested_map function"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand(
            [
               ({}, ("a")),
               ({"a": 1}, ("a", "b"))])
    def test_access_nested_map_exception(self, nested_map: Dict, path: Tuple):
        """method tests if the exception is raised"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Class Tests get_json method from utils.py"""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
        ])
    def test_get_json(self, test_url: str, expected: Dict):
        """Method tests get_json"""
        mock_get = Mock()
        mock_get.json.return_value = expected

        with patch("requests.get", return_value=mock_get) as mock_request:
            result = get_json(test_url)
            self.assertEqual(result, expected)
            mock_request.assert_called_once()


class TestMemoize(unittest.TestCase):
    """class tests memoize method from utils module"""
    def test_memoize(self):
        """Method tests memoize"""
        class TestClass:
            """test class"""
            def a_method(self):
                """Returns 42"""
                return 42

            @memoize
            def a_property(self):
                """Retruns a memoized value"""
                return self.a_method()

        with patch.object(TestClass, "a_method",
                          return_value=42) as mock_method:
            test_class = TestClass()
            result = test_class.a_property
            result = test_class.a_property
            self.assertEqual(result, 42)
            mock_method.assert_called_once()
