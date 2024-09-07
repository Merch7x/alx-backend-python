#!/usr/bin/env python3
"""Implementing unit test through the
   unittest module
"""
from utils import access_nested_map, get_json
import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """ Tests various method functionalities"""
    @parameterized.expand([
      ({"a": 1}, ("a",), 1),
      ({"a": {"b": 2}}, ("a",), {"b": 2}),
      ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_acccess_nested_map(self, nested_map, path, expected):
        """Test whether path leads to key accurately"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested, path):
        """Test wether exceptions are raised"""
        with self.assertRaises(KeyError):
            access_nested_map(nested, path)


class TestGetJson(unittest.TestCase):
    """Use mocking to test external requests"""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, url, payload, mock_get):
        """Test whether function returns json"""

        mock_response = MagicMock()
        mock_response.json.return_value = payload
        mock_get.return_value = mock_response

        result = get_json(url)

        self.assertEqual(result, payload)

        mock_get.assert_called_once_with(url)
