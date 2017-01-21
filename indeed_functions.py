#!/usr/bin/python3

"""
                    Indeed.com Job Search Functions
    Author: Zach Churchill
    Python Version: 3.5.2
    Description: Functions used specifically to format and open job postings
        from Indeed.com - thus, some values such as the location format, base
        url, and HTML tags have been hardcoded. 
"""

import re
import sys
import requests
import webbrowser
from bs4 import BeautifulSoup


def format_location(user_data):
    """Formats the city and state into the format required by the url for
    Indeed.com.

    Parameters
    ==========
    user_data (dict) : Dict of user data with keys corresponding the state and
        city.

    Returns
    =======
    location (str) : String containing the city and state abbreviation
        in the corresponding places in the location_format parameter.

    """
    location_format = "{city}%2C+{state}"
    location = location_format.format(**user_data)
    return location

def format_search_terms(user_data):
    """Formats the city and state into the format required by the url for
    Indeed.com.

    Parameters
    ==========
    user_data (dict) : Dict of user data with a key corresponding to the search
        terms.

    Returns
    =======
    search_terms_str (str) : String containing the search terms entered by the
        user with +'s in each space, i.e. ['Python', 'Data science'] ->
        'Python+Data+science'.

    """
    input_terms = user_data["search_terms"]
    # First, add +'s inbetween terms with phrases
    search_terms = ['+'.join(term.split()) for term in input_terms]
    # Then, add +'s inbetween the terms themselves
    search_terms_str = '+'.join(search_terms)
    return search_terms_str


def prepare_url(user_data):
    """Prepares the base url of Indeed.com with the possible search terms.

    Parameters
    ==========
    user_data (dict) : Dict of user data with a key corresponding to the search
        terms and location.

    Returns
    =======
    page_url (str) : String of url with search terms.

    """
    base_url = "https://www.indeed.com/jobs?q={search_terms_str}&l={location}"
    page_url = base_url.format(**user_data)
    return page_url


def request_page(page_url):
    """Requests the page given by the page url and returns the page content
    as a BeautifulSoup object if successful; otherwise, exits the program.

    Parameters
    ----------
    page_url (str) : String containing the url address for the page.

    Returns
    -------
    BeautifulSoup object of the page content.

    """
    try:
        page = requests.get(page_url)
    except requests.exceptions.ConnectionError:
        print("ERROR: CONNECTION ERROR FOR GIVEN URL")
        sys.exit()
    else:
        if page.status_code == 200:
            return BeautifulSoup(page.content, "lxml")
        else:
            print("REQUEST ERROR {}".format(page.status_code))
            sys.exit()


def job_search_results(soup, num_search_results):
    """Retrives the number of results from Indeed.com (by relevance).

    Parameters
    ----------
    soup (BeautifulSoup) : BeautifulSoup object containing the HTML for
        the given location and search terms for the job search.

    num_search_results (int) : Integer representing the number of search
        results that the user desires to see.

    """
    counter = 0
    for link in soup.find_all("a", {"data-tn-element": "jobTitle"}):
        if counter < num_search_results:
            job_url = "https://www.indeed.com" + link.get("href")
            webbrowser.open(job_url, new=0, autoraise=False)
            counter += 1
        else:
            break
