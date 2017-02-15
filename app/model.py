#!/usr/bin/python3

"""
                Model portion of MVC for Indeed Job Search App
    Author: Zach Churchill
    Python Version: 3.5.2
    Description: This file contains the Indeed App model. Within this model is
        the necessary data to perform a basic search on Indeed.com, where the
        data necessary are the location, search terms and number of results.
        Moreover, the model contains the necessary functions that are needed to
        interact with Indeed.com itself through the use of requests, webbrowser,
        and BeautifulSoup via hardcoded data like the url and the required
        format of the location and search terms.
"""

import sys
import requests
import webbrowser
from bs4 import BeautifulSoup

class IndeedAppModel(object):
    """Representation of the necessary data and functions needed to interact
    with Indeed.com.

    """
    def __init__(self):
        url = "https://www.indeed.com/jobs?q={search_terms}&l={location}"
        self.url = url

    def _format_location(*, city, state):
        """Formats the city and state into the format required by the url for
         Indeed.com.

        Parameters
        ==========
        city (str) : String corresponding to the city entered by the user.
        state (str) : String corresponding to the state abbreviation chosen by
            the user in the view GUI.

        Returns
        =======
        location (str) : String containing the city and state abbreviation
            in the corresponding places in the location_format parameter.

        """
        location_format = "{city}%2C+{state}"
        location = location_format.format(city=city, state=state)
        return location

    def _format_search_terms(search_terms):
        """Formats the city and state into the format required by the url for
        Indeed.com.

        Parameters
        ==========
        search_terms (list) : List of strings corresponding to the search terms
            entered by the user in the view GUI.

        Returns
        =======
        search_terms_str (str) : String containing the search terms entered by
            the user with +'s in each space, i.e. ['Python', 'Data science'] ->
            'Python+Data+science'.

        """
        # First, add +'s inbetween terms with phrases
        search_terms = ['+'.join(term.split()) for term in search_terms]
        # Then, add +'s inbetween the terms themselves
        search_terms_str = '+'.join(search_terms)
        return search_terms_str

    def _prepare_url(self):
        """Prepares the base url of Indeed.com with the possible search terms.

        Parameters
        ==========
        user_data (dict) : Dict of user data with a key corresponding to the
            search terms and location.

        Returns
        =======
        page_url (str) : String of url with search terms.

        """
        user_data = {"location": self.location, \
                     "search_terms": self.search_terms}
        page_url = self.url.format(**user_data)
        return page_url

    def initialize_data(self, *, city, state, search_terms, num_results):
        """Provides a setter function for the controller to call once the data
        is retrieved from the view. The location and search terms are
        immediately formatted according to the standards set by Indeed.com.

        Parameters (All are keyword enforced)
        ==========
        city (str) : String corresponding to the city name that the user
            entered into the text field of the view GUI.
        state (str) : String corresponding to the state abbreviation that the
            user chose in the view GUI.
        search_terms (list) : List of strings separated by commas corresponding
            to the search terms that were entered by the user in the text field
            of the view GUI.
        num_results (int) : Integer corresponding to the number of results that
            the user chose from the view GUI.

        """
        self.location = IndeedAppModel._format_location(city=city, state=state)
        self.search_terms = IndeedAppModel._format_search_terms(search_terms)
        self.num_results = num_results
        self.page_url = self._prepare_url()

    def request_page(self):
        """Requests the page given by the page url and creates a soup variable,
        which is the page content as a BeautifulSoup object, if successful;
        otherwise, exits the program.

        """
        try:
            page = requests.get(self.page_url)
        except requests.exceptions.ConnectionError:
            print("ERROR: CONNECTION ERROR FOR GIVEN URL")
            sys.exit()
        else:
            if page.status_code == 200:
                self.soup = BeautifulSoup(page.content, "lxml")
            else:
                print("REQUEST ERROR {}".format(page.status_code))
                sys.exit()

    def _extract_job_urls(self):
        """Retrieves the number of results from Indeed.com (by relevance).

        Parameters
        ==========
        soup (BeautifulSoup) : BeautifulSoup object containing the HTML for
            the given location and search terms for the job search.

        Returns
        ==========
        job_urls (list) : List of strings corresponding to URLs for jobs.

        """
        home_url = "https://www.indeed.com"
        job_urls = []
        job_titles = self.soup.find_all("a", {"data-tn-element": "jobTitle"})
        for link in job_titles[:self.num_results]:
            job_urls.append(home_url + link.get("href"))
        return job_urls

    def display_job_search_results(self):
        """Opens the job urls in a new (default) browser of the machine.

        Parameters
        ==========
        job_urls (list) : List of strings corresponding to URLs for jobs.

        """
        job_urls = self._extract_job_urls()
        for job_url in job_urls:
            webbrowser.open(job_url, new=1)
