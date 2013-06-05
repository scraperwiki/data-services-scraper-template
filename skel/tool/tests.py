#!/usr/bin/env python

import unittest
from collections import OrderedDict
from os.path import join, dirname, abspath

from main import process


class ScraperTestCase(unittest.TestCase):
    def setUp(self):
        """
        Run before each and every test method.
        """
        filename = join(
            dirname(abspath(__file__)),
            'sample_data/simple.html')
        with open(filename, 'rb') as f:
            self.simple_html = f.read()

    def tearDown(self):
        """
        """
        pass

    def test_assert_equal_one(self):
        self.assertEqual(2, 1 + 1)

    def test_assert_raises(self):
        empty_list = []
        self.assertRaises(IndexError, lambda: empty_list[2])

    def test_process_yields_rows(self):
        row_generator = process(self.simple_html)
        self.assertIsInstance(row_generator.next(), OrderedDict)
