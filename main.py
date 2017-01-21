#!/usr/bin/python3

import sys
import tkinter as tk
from data_retrieval_app import GetDataApp
from indeed_functions import format_location, format_search_terms
from indeed_functions import prepare_url, request_page, job_search_results

def get_user_data():
    """Retrieves the users data via the GetDataApp GUI; otherwise, exits the
    program (if user quits the GUI).

    Returns
    =======
    user_data (dict) : A dictionary with keys corresponding to the city, state,
        search terms, and number of search results obtained from the GUI.

    """
    root = tk.Tk()
    user_data_app = GetDataApp(root)
    user_data_app.mainloop()

    try:
        user_data = user_data_app.get_data()
    except AttributeError:
        sys.exit()
    else:
        return user_data

def main():
    user_data = get_user_data()
    user_data["location"] = format_location(user_data)
    user_data["search_terms_str"] = format_search_terms(user_data)

    page_url = prepare_url(user_data)
    soup = request_page(page_url)
    job_search_results(soup, user_data["num_results"])

if __name__ == "__main__":
    main()
