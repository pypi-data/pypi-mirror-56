#!/usr/bin/env python

"""Tests for `harrpy` package."""

import unittest

from harrpy import harrpy


class TestHarrpy(unittest.TestCase):
    """Tests for `harrpy` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        self.assertEqual(harrpy.hello_harrpy(), "foo")


if __name__ == "__main__":
    unittest.main()
