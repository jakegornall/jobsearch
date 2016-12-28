#!/usr/bin/python3

"""
    Title: Test Suite for jobsearch.py
    Author: Zach Churchill
    Date: 12/23/16
    Description: Unit tests for each of the functions in the 
        jobsearch.py file. Run this test as follows:
        python3 test_jobsearch.py -b
        where the -b tag supresses stout buffer.
"""

import unittest
from unittest.mock import patch
from io import StringIO # Used to retrieve output printed to screen
from itertools import chain # Used for multiple user inputs
from jobsearch import get_location, get_search_terms, get_num_search_results
from jobsearch import prepare_url

class TestLocationInput(unittest.TestCase):
    """Tests the get_location function for situations where there are no
    spelling errors and with spelling errors the first time data in input.
    
    """
    no_spelling_errors = ["Columbus", "OH", "Y"]
    spelling_error = ["Renoc", "NV", "N", "Reno", "NV", "Y"]

    def setUp(self):
        self.location_format = "{city}%2C+{state}"

    @patch("builtins.input", side_effect=chain(no_spelling_errors))
    def test_no_spelling_errors(self, mock_user_inputs):
        self.location = get_location(self.location_format)
        self.assertEqual(self.location, "Columbus%2C+OH")

    @patch("builtins.input", side_effect=chain(spelling_error))
    def test_with_spelling_error(self, mock_user_inputs):
        self.location = get_location(self.location_format)
        self.assertEqual(self.location, "Reno%2C+NV")


class TestGetSearchTerms(unittest.TestCase):
    """Tests the get_search_terms() function for situations where there
    is no input, only one word, and multiple words in one search term,
    i.e. human resources.
    Note: The word 'done' signifies that the user is finished typing search
    terms into the script.

    """

    no_search_terms = ["done"]
    one_search_term = ["communications", "done"]
    multiple_words_term = ["public relations", "done"]

    @patch("builtins.input", side_effect=chain(no_search_terms))
    def test_no_terms(self, mock_user_input):
        self.get_no_terms = get_search_terms()
        self.assertEqual(self.get_no_terms, "")

    @patch("builtins.input", side_effect=chain(one_search_term))
    def test_one_term(self, mock_user_input):
        self.get_one_term = get_search_terms()
        self.assertEqual(self.get_one_term, "communications")

    @patch("builtins.input", side_effect=chain(multiple_words_term))
    def test_multiple_words_term(self, mock_user_input):
        self.get_multiple_words_term = get_search_terms()
        self.assertEqual(self.get_multiple_words_term, "public+relations")


class TestGetNumSearchResults(unittest.TestCase):
    """Tests the get_num_search_results() function for the following 
    situations: character instead of integer for first entry, negative
    integer for first entry, integer greater than 10 for first entry, 
    and lastly an integer between 0 and 10.

    """
    character_first = ['a', '1']
    negative_num_first = ['-1', '1']
    greater_than_ten_first = ['11', '1']
    correct_num_first = ['1']

    @patch("builtins.input", side_effect=chain(character_first))
    def test_character_input_first(self, mock_user_input):
        self.num_results = get_num_search_results()
        self.assertEqual(self.num_results, 1)

    @patch("builtins.input", side_effect=chain(negative_num_first))
    def test_negative_num_input_first(self, mock_user_input):
        self.num_results = get_num_search_results()
        self.assertEqual(self.num_results, 1)

    @patch("builtins.input", side_effect=chain(greater_than_ten_first))
    def test_num_greater_than_ten_input_first(self, mock_user_input):
        self.num_results = get_num_search_results()
        self.assertEqual(self.num_results, 1)

    @patch("builtins.input", side_effect=chain(correct_num_first))
    def test_correct_input_first(self, mock_user_input):
        self.num_results = get_num_search_results()
        self.assertEqual(self.num_results, 1)


class TestPrepareURL(unittest.TestCase):
    """Tests the prepare_url() function for the following cases where it is
    assumed that the base_url parameter is hardcoded into the main(): 
    user_data parameter is an empty dict, user_data is missing the location, 
    user_data is missing the search_terms, and finally when all of the data 
    is supplied correctly.
    
    """

    def setUp(self):
        """Sets up a pretend URL with places to format in location and
        search terms for testing.
        
        """
        self.base_url = "www.someURL.com/jobs?q={location}&2={search_terms}"
        self.user_data = {"location": "Reno%2C+NV",
                          "search_terms": "data+science+python"}

    def test_empty_user_data(self):
        """Tests the output that is printed to the screen when user_data is 
        an empty dictionary, and that the SystemExit exception is called.
        
        """
        expected_msg = """[] keys supplied, but ['location', 'search_terms']
                           keys needed."""
        with patch("sys.stdout", new=StringIO()) as msg:
            with self.assertRaises(SystemExit) as excptn:
                prepare_url(self.base_url, {})
                self.assertEqual(msg.get_value(), expected_msg)

    def test_missing_location(self):
        """Tests the output that is printed to the screen when user_data only 
        contains the search terms, and that the SystemExit exception is 
        called.
        
        """
        expected_msg = """['search_terms'] keys supplied, but ['location', 
                           'search_terms'] keys needed."""
        with patch("sys.stdout", new=StringIO()) as msg:
            with self.assertRaises(SystemExit) as excptn:
                prepare_url(self.base_url, {})
                self.assertEqual(msg.get_value(), expected_msg)

    def test_missing_search_terms(self):
        """Tests the output that is printed to the screen when user_data only 
        contains the location, and that the SystemExit exception is called.
        
        """
        expected_msg = """['location'] keys supplied, but ['location', 
                           'search_terms'] keys needed."""
        with patch("sys.stdout", new=StringIO()) as msg:
            with self.assertRaises(SystemExit) as excptn:
                prepare_url(self.base_url, {})
                self.assertEqual(msg.get_value(), expected_msg)

    def test_correct_info_supplied(self):
        """Tests that the returned URL is correct given the correct input 
        variables for the parameters.

        """
        page_url = self.base_url.format(**self.user_data)
        self.assertEqual(prepare_url(self.base_url, self.user_data), page_url)

if __name__ == "__main__":
    unittest.main(exit=False)
        
