#!/usr/bin/env python3
"""Implementing unittests through the
   unittest module
"""
from client import GithubOrgClient
import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    """Test requests to an external server"""

    @parameterized.expand([
        ("google", {"payload": True}),
        ("abc", {"payload": False}),
    ])
    @patch('requests.get')
    def test_org(self, org_name, payload, mock_get):
        """test org returns a json payload using get_json"""
        mock_response = MagicMock()
        mock_response.json.return_value = payload
        mock_get.return_value = mock_response

        result = GithubOrgClient(org_name).org

        self.assertEqual(result, payload)

        mock_get.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test that the repos_url is equal to that in the
        property dict
        """
        with patch.object(GithubOrgClient, 'org',
                          new_callable=PropertyMock)as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos"}

            client = GithubOrgClient("google")
            result = client._public_repos_url
            self.assertEqual(
                result, "https://api.github.com/orgs/google/repos")
            mock_org.assert_called_once()

    @patch('requests.get')
    def test_public_repos(self, mock_get):
        """Test a list of repo names in payload"""
        mock_get.return_value.json.return_value = [
            {"name": "home"},
            {"name": "away"},
        ]

        with patch.object(GithubOrgClient, '_public_repos_url',
                          new_callable=PropertyMock)as mock_public_repo_url:
            mock_public_repo_url.return_value =\
                "https://api.github.com/orgs/google/repos"

            client = GithubOrgClient("google")
            result = client.public_repos()
            self.assertEqual(result, ["home", "away"])
            mock_public_repo_url.assert_called_once()
            mock_get.assert_called_once_with(
                "https://api.github.com/orgs/google/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, lkey, expected):
        """Test whether a repo has a LICENSE"""
        self.assertEqual(GithubOrgClient.has_license(repo, lkey), expected)
