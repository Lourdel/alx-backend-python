#!/usr/bin/env python3
"""Module defines TestAccessNestedMap"""

import unittest
from typing import Tuple, Dict, Union
from parameterized import parameterized
from unittest.mock import patch, Mock
access_nested_map = __import__("utils").access_nested_map
get_json = __import__("utils").get_json


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
