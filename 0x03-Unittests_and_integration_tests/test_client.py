#!/usr/bin/env python3
"""Module defines GithubOrgclient test methods"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from typing import Dict
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """class tests GithubOrgClient"""
    @parameterized.expand([
        ("google", {"id": 256}),
        ("abc", {"id": 244})
        ])
    @patch("client.get_json")
    def test_org(self, org: str, expected: Dict, mock_org: Mock) -> None:
        """Method tests org function"""
        mock_org.return_value = expected
        mock_obj = GithubOrgClient(org)
        self.assertEqual(mock_obj.org, expected)
        mock_org.assert_called_once_with("https://api.github.com/orgs/" + org)

    def test_public_repos_url(self):
        """Method tests _public_repos_url"""
        expected = "https://api.github.com/orgs/repo"
        payload = {"repos_url": "https://api.github.com/orgs/repo"}
        with patch('client.GithubOrgClient.org', PropertyMock(
                    return_value=payload)):
            obj = GithubOrgClient("Google")
            self.assertEqual(obj._public_repos_url, expected)

    @patch("client.get_json")
    def test_public_repos(self, mock_obj: Mock):
        """Method tests _public_repos property"""
        expected = {"Command": "git_pull"}
        mock_obj.return_value = expected

        result = "github.com/google"
        with patch("client.GithubOrgClient._public_repos_url", PropertyMock(
                    return_value=result)) as mock_repo:
            obj = GithubOrgClient("google")
            self.assertEqual(obj._public_repos_url, result)
