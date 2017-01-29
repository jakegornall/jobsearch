#!/usr/bin/python3

import sys
import tkinter as tk
from data_retrieval_app import get_user_data, GetDataApp
import indeed

def main():
    data = get_user_data()
    data["location"] = indeed.format_location(data)
    data["search_terms_str"] = indeed.format_search_terms(data)

    page_url = indeed.prepare_url(data)
    soup = indeed.request_page(page_url)
    job_urls = indeed.retrieve_job_search_results(soup, data["num_results"])
    indeed.display_job_search_results(job_urls)

if __name__ == "__main__":
    main()
