#!/usr/bin/env python3
"""Module defines GithubOrgclient test methods"""

import unittest
from unittest.mock import patch, Mock, PropertyMock, call
from typing import Dict
from parameterized import parameterized, parameterized_class
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

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False)
        ]
    )
    def test_has_license(self, repo: Dict[str, Dict],
                         license_key: str, expected: bool):
        """tests _has_license Method"""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key),
                         expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Class Implements intergration tests for public_repos method"""

    @classmethod
    def setUpClass(clas):
        """Method sets up test params"""
        org = TEST_PAYLOAD[0][0]
        repos = TEST_PAYLOAD[0][1]
        org_mock = Mock()
        org_mock.json = Mock(return_value=org)
        clas.org_mock = org_mock
        repos_mock = Mock()
        repos_mock.json = Mock(return_value=repos)
        clas.repos_mock = repos_mock

        clas.get_patcher = patch('requests.get')
        clas.get = clas.get_patcher.start()
        options = {clas.org_payload["repos_url"]: repos_mock}
        clas.get.side_effect = lambda y: options.get(y, org_mock)

    @classmethod
    def tearDownClass(clas):
        """ Method cleans up resources after test """
        clas.get_patcher.stop()

    def test_public_repos(self):
        """ Method tests public repos"""
        y = GithubOrgClient("x")
        self.assertEqual(y.org, self.org_payload)
        self.assertEqual(y.repos_payload, self.repos_payload)
        self.assertEqual(y.public_repos(), self.expected_repos)
        self.assertEqual(y.public_repos("NONEXISTENT"), [])
        self.get.assert_has_calls([call("https://api.github.com/orgs/x"),
                                   call(self.org_payload["repos_url"])])

    def test_public_repos_with_license(self):
        """Method tests public repos with licence"""
        y = GithubOrgClient("x")
        self.assertEqual(y.org, self.org_payload)
        self.assertEqual(y.repos_payload, self.repos_payload)
        self.assertEqual(y.public_repos(), self.expected_repos)
        self.assertEqual(y.public_repos("NONEXISTENT"), [])
        self.assertEqual(y.public_repos("apache-2.0"), self.apache2_repos)
        self.get.assert_has_calls([call("https://api.github.com/orgs/x"),
                                   call(self.org_payload["repos_url"])])
