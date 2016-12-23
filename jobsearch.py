#!/usr/bin/python3

"""Contains a procedural approach to scraping job postings from Indeed.com."""

import re
import sys
import requests
import webbrowser
from bs4 import BeautifulSoup

def prepare_url(base_url, search_terms):
    """Prepares the base url of Indeed.com with the possible search terms.

    Parameters
    ----------
    base_url (str) : Pre-formatted string with places to add search terms
        using keyword arguments.
    
    search_terms (dict) : Dict of keys corresponding to the format keyword
        arguments in the base url.

    Returns
    -------
    page_url (str) : String of url with search terms.

    """
    try:
        page_url = base_url.format(**search_terms)
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
    page = requests.get(page_url)
    if page.status_code == 200:
        return BeautifulSoup(page.content, "lxml")
    else:
        print("REQUEST ERROR {}".format(page.status_code))
        sys.exit()


def job_search_results(soup):
    """Retrives the top 5 results from Indeed.com by relevance.

    Parameters
    ----------
    soup (BeautifulSoup) : BeautifulSoup object containing the HTML for
        the given location and search terms for the job search.
    """
    counter = 0
    for link in soup.find_all("a", {"data-tn-element": "jobTitle"}):
        if counter < 5:
            job_url = "https://www.indeed.com" + link.get("href")
            webbrowser.open(job_url, new=0, autoraise=True)
            counter += 1
        else:
            break


def main():
    base_url = "https://www.indeed.com/jobs?q={search_terms}&l={city}"
    search_terms = {"city": "Columbus%2C+OH", 
                    "search_terms": "communications+human+resources"}

    page_url = prepare_url(base_url, search_terms)
    soup = request_page(page_url)
    job_search_results(soup)


if __name__ == "__main__":
    main()
