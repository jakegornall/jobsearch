#!/usr/bin/python3

"""
    Title: Indeed.com Job Search Script
    Author: Zach Churchill
    Date: 12/22/16
    Description: Displays the top search results from Indeed.com based on
        search terms and location given by the user in the default browser.
"""

import re
import sys
import requests
import webbrowser
from bs4 import BeautifulSoup


def get_location(location_format):
    """Prompts the user for the location to use in the job search.

    Parameters
    ----------
    location_format (str) : Formatted string with the correct placement
        of the city and and state abbreviation.

    Returns
    -------
    location (str) : String containing the city and state abbreviation
        in the corresponding places in the location_format parameter.

    """
    city_prompt = "Enter the city: "
    state_prompt = "Enter the state abbreviation, i.e. OH for Ohio: "
    while True:
        city_input = input(city_prompt)
        state_input = input(state_prompt)
        if len(state_input) == 2:
            check_prompt = "Is {}, {} correct? (Y/N)\n-> "
            check_input = input(check_prompt.format(city_input, state_input))
            if check_input.lower() == 'y':
                break
            else:
                print("Let's try again.\n")

    location = location_format.format(city=city_input, state=state_input)
    return location


def get_search_terms():
    """Prompts the user for the search terms to be used in the job search.

    Returns
    -------
    search_terms (str) : Search terms given by user in a string with +'s
        instead of spaces, e.g. search terms given by the user are 
        ["human resources", "communications"], so the the search_terms 
        string returned is "human+resources+communications".

    """
    input_terms = []
    search_terms_prompt = "Enter a search term (enter 'done' when finished): "
    finished = False
    while not finished:
        search_term = input(search_terms_prompt)
        if search_term.lower() == 'done':
            finished = True
        else:
            input_terms.append(search_term)

    # First, add +'s inbetween terms with phrases
    search_terms_list = ['+'.join(term.split()) for term in input_terms]
    # Then, add +'s inbetween the terms themselves
    search_terms = '+'.join(search_terms_list)

    return search_terms


def get_num_search_results():
    """Prompts user to input the number of search results desired, with a 
    limit of 10.

    Returns
    -------
    num_search_results (int) : Integer representing the number of search
        results that the user desires to see.

    """
    search_results_prompt = "Enter the number of search results desired: "
    while True:
        num_results = input(search_results_prompt)
        try:
            num_results = int(num_results)
        except TypeError:
            print("ERROR: Enter a number.\n")
        else:
            if num_results < 10:
                break

    print("{} results will be retrieved momentarily.".format(num_results))
    return num_results


def prepare_url(base_url, user_data):
    """Prepares the base url of Indeed.com with the possible search terms.

    Parameters
    ----------
    base_url (str) : Pre-formatted string with places to add search terms
        using keyword arguments.
    
    user_data (dict) : Dict of keys corresponding to the format keyword
        arguments in the base url.

    Returns
    -------
    page_url (str) : String of url with search terms.

    """
    try:
        page_url = base_url.format(**user_data)
    except KeyError:
        url_list = []
        last = 0
        for braces in re.finditer('{\w*}', base_url):
            url_list.append(base_url[last:braces.span()[0]])
            last = braces.span()[1]
        page_url = ''.join(url_list)
        pass
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
    """Retrives the top 5 results from Indeed.com by relevance.

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
            webbrowser.open(job_url, new=0, autoraise=True)
            counter += 1
        else:
            break


def main():
    # Get user input for location and search terms for job search.
    location_format = "{city}%2C+{state}"
    location = get_location(location_format)
    search_terms = get_search_terms()
    num_search_results = get_num_search_results()

    base_url = "https://www.indeed.com/jobs?q={search_terms}&l={location}"
    user_data = {"location": location, "search_terms": search_terms}

    page_url = prepare_url(base_url, user_data)
    soup = request_page(page_url)
    job_search_results(soup, num_search_results)


if __name__ == "__main__":
    main()
