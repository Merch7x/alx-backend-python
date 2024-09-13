#!/usr/bin/env python3
"""Implementing unittests through the
   unittest module
"""
from client import GithubOrgClient
import unittest
from unittest.mock import patch, MagicMock
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
