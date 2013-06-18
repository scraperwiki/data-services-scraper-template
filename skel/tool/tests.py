#!/usr/bin/env python

import unittest
from collections import OrderedDict
from os.path import join, dirname, abspath

from main import process

SAMPLE_DIR = join(dirname(abspath(__file__)), 'sample_data')


class ScraperTestCase(unittest.TestCase):
    def setUp(self):
        """Run before each and every test method."""
        pass

    def tearDown(self):
        """Run afte reach and every test method"""
        pass

    def test_assert_raises(self):
        empty_list = []
        self.assertRaises(IndexError, lambda: empty_list[2])

    def test_process_simple_html_yields_rows(self):
        with open(join(SAMPLE_DIR, 'simple.html'), 'r') as f:
            row_generator = process(f)
            self.assertIsInstance(row_generator.next(), OrderedDict)
