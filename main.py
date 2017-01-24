#!/usr/bin/python3

import sys
import tkinter as tk
from data_retrieval_app import get_user_data, GetDataApp
from indeed_functions import format_location, format_search_terms
from indeed_functions import prepare_url, request_page, job_search_results

def main():
    user_data = get_user_data()
    user_data["location"] = format_location(user_data)
    user_data["search_terms_str"] = format_search_terms(user_data)

    page_url = prepare_url(user_data)
    soup = request_page(page_url)
    job_search_results(soup, user_data["num_results"])

if __name__ == "__main__":
    main()
