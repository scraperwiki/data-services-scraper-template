#!/usr/bin/env python
# encoding: utf-8

import unittest
from nose.tools import assert_equal
from os.path import join, dirname, abspath

from main import process

SAMPLE_DIR = join(dirname(abspath(__file__)), 'sample_data')


class ScraperTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Run once before all tests in this test class."""
        with open(join(SAMPLE_DIR, 'sample_data.html'), 'r') as f:
            cls.rows = list(process(f))

    def test_correct_number_of_rows(self):
        assert_equal(10, len(self.rows))
