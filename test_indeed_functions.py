#!/usr/bin/python3

"""
                    Unit Tests for indeed_functions.py
    Author: Zach Churchill
    Python Version: 3.5.2
    Description: Unit tests for all of the functions that are able to
        be tested in the indeed_functions.py.
"""

import unittest
from unittest.mock import patch
from io import StringIO # Used to retrieve output printed to screen
from itertools import chain # Used for multiple user inputs
from indeed_functions import format_location, format_search_terms
from indeed_functions import prepare_url, request_page, job_search_results

class TestFormatLocation(unittest.TestCase):
    def setUp(self):
        self.user_data = {"state": "OH", "city": "athens"}

    def test_format_location(self):
        test_output = "athens%2C+OH"
        self.assertEqual(format_location(self.user_data), test_output)


class TestFormatSearchTerms(unittest.TestCase):
    def setUp(self):
        self.user_data = {"search_terms": ["Python", "Web Development"]}

    def test_format_search_terms(self):
        test_output = "Python+Web+Development"
        self.assertEqual(format_search_terms(self.user_data), test_output)


class TestPrepareURL(unittest.TestCase):
    def setUp(self):
        self.user_data = {"location": "athens%2C+OH",
                          "search_terms_str": "Python+Web+Development"}

    def test_prepare_url(self):
        test_output = "https://www.indeed.com/jobs?q="
        test_output += "Python+Web+Development&l=athens%2C+OH"
        self.assertEqual(prepare_url(self.user_data), test_output)


if __name__ == "__main__":
    unittest.main(exit=False)
