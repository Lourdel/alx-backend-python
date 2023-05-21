#!/usr/bin/env python3
"""Module defines GithubOrgclient test methods"""

import unittest
from unittest.mock import patch, Mock
from typing import Dict
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """class tests GithubOrgClient"""
    @parameterized.expand([
        ("google", {"id": 256}),
        ("abc", {"id": 244})
        ])
    @patch("client.get_json")
    def test_org(self, org: str, expected: Dict, mock_org: Mock):
        """Method tests org function"""
        mock_org.return_value = expected
        mock_obj = GithubOrgClient(org)
        self.assertEqual(mock_obj.org, expected)
        mock_org.assert_called_once_with(f"https://api.github.com/orgs/{org}")
