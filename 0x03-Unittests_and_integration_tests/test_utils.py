#!/usr/bin/env python3
"""Module defines TestAccessNestedMap"""

import unittest
from typing import Tuple, Dict, Union
from parameterized import parameterized
access_nested_map = __import__("utils").access_nested_map


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
