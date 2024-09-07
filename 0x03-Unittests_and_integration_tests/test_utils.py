#!/usr/bin/env python3
"""Implementing unit test through the
   unittest module
"""
from utils import access_nested_map
import unittest
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """ Tests various method functionalities"""
    @parameterized.expand([
      ({"a": 1}, ("a",), 1),
      ({"a": {"b": 2}}, ("a",), {"b": 2}),
      ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_acccess_nested_map(self,
                                nested_map: map, path: tuple, expected: str):
        """Test whether path leads to key accurately"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    # @parameterized.expand([
    #     ({}, ("a",)),
    #     ({"a": 1}, ("a", "b")),
    # ])
    # def test_access_nested_map_exception(self, nested, path):
    #     """Test wether exceptions are raised"""
    #     with self.assertRaises(KeyError):
    #         access_nested_map(nested, path)
