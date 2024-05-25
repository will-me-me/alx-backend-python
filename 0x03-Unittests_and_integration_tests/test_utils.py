#!/usr/bin/env python3
"""Utils Unittest Module."""
import unittest
from parameterized import parameterized
from typing import Sequence, Mapping
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch


class TestAccessNestedMap(unittest.TestCase):
    """All unittest cases for access_nested_map function in the utils module"""

    @parameterized.expand([
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
            ])
    def test_access_nested_map(self, nested_map: Mapping,
                               path: Sequence, expected):
        """Testd if access nested map return the rightful output"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a", )),
        ({"a": 1}, ("a", "b"))
        ])
    def test_access_nested_map_exception(self, nested_map: Mapping,
                                         path: Sequence):
        """Tests if exception is being raised for the wrong argument"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """All unittest cases for get_json function in the utils module"""

    @parameterized.expand([
        ('http://example.com', {"payload": True}),
        ('http://holberton.io', {"payload": False})
        ])
    @patch('utils.requests')
    def test_get_json(self, test_url: str, test_payload: Mapping, mock_req):
        """Test if get_json returns the rightful output"""
        mock_req.get.return_value.json.return_value = test_payload
        self.assertEqual(get_json(test_url), test_payload)


class TestMemoize(unittest.TestCase):
    """All unittest cases for memoize function in utils module"""
    def test_memoize(self):
        """Check if a method is memoized"""
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()
        test_inst = TestClass()
        with patch.object(
                TestClass, 'a_method', return_value=42) as mock_a_method:
            res1 = test_inst.a_property
            res2 = test_inst.a_property
            mock_a_method.assert_called_once()
            self.assertEqual(res1, 42)
            self.assertEqual(res2, 42)
