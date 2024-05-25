#!/usr/bin/env python3
"""Client Unittest Module."""
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import unittest
from unittest.mock import patch, Mock
from typing import Dict
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """All test cases the client script."""

    @parameterized.expand([
        'google',
        'abc'
        ])
    @patch('client.get_json')
    def test_org(self, org: str, mock_get_json):
        """Test if org the method from GithubOrgClient returns the right output."""
        expect = {
                "repo_url": f"https://api.github.com/orgs/{org}"
                }
        mock_get_json.return_value = expect
        git_org = GithubOrgClient(org)
        self.assertEqual(git_org.org, expect)

    def test_public_repos_url(self):
        """Test if org the method from GithubOrgClient return the right output."""
        with patch.object(GithubOrgClient,
                          '_public_repos_url') as mock_public_repos_url:
            expect = 'https://api.github.com/orgs/google/repos'
            git_org = GithubOrgClient('google')
            mock_public_repos_url.__get__ = Mock(return_value=expect)
            self.assertEqual(git_org._public_repos_url, expect)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test if the org method from GithubOrgClient return the right output"""
        for org in ['google', 'abc']:
            expect = {
                    "repo_url": f"https://api.github.com/orgs/{org}"
                    }
            mock_get_json.return_value = expect
            with patch.object(GithubOrgClient,
                              '_public_repos_url') as mock_public_repos_url:
                git_org = GithubOrgClient(org)
                self.assertEqual(git_org.org, expect)
                expect = f'https://api.github.com/orgs/{org}/repos'
                mock_public_repos_url.__get__ = Mock(return_value=expect)
                self.assertEqual(git_org._public_repos_url, expect)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "my_other_license"}}, "my_license", False)
        ])
    def test_has_license(self, repo: Dict[str, Dict],
                         license_key: str, expect: bool):
        """Test if the org method from GithubOrgClient return the right output"""
        git_org = GithubOrgClient('google')
        self.assertEqual(git_org.has_license(repo, license_key), expect)


@parameterized_class(('org_payload', 'repos_payload',
                      'expected_repos', 'apache2_repos'), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for Github Org Client"""

    @classmethod
    def setUpClass(cls):
        """This sets the env for each test"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.return_value.json.side_effect = [
                cls.org_payload, cls.repos_payload,
                cls.org_payload, cls.repos_payload
                ]

    @classmethod
    def tearDownClass(cls):
        """Tear down"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test if the org method from GithubOrgClient return the right output."""
        client = GithubOrgClient('google')
        repos = client.public_repos()
        self.assertEqual(len(repos), len(self.expected_repos))
        for repo in repos:
            self.assertIn(repo, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test if the org method from GithubOrgClient return the right output"""
        client = GithubOrgClient('google')
        repos = client.public_repos("apache-2.0")
        self.assertEqual(len(repos), len(self.apache2_repos))
        for repo in repos:
            self.assertIn(repo, self.apache2_repos)
