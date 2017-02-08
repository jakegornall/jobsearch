#!/usr/bin/python3

"""
                Controller portion of MVC for Indeed Job Search App
    Author: Zach Churchill
    Python Version: 3.5.2
    Description: This file contains the Indeed App controller. The controller
        will act as the liaison between the view and model, where the view
        retrieves the data from the user via the GUI, and the model stores said
        data to perform tasks on it.
"""

import sys
from app import IndeedAppModel
from app import IndeedAppView

class IndeedAppController(object):

    def __init__(self):
        self.model = IndeedAppModel()
        self.view = IndeedAppView()

    def start_app(self):
        """Runs the whole app by first running the view GUI, and then if the
        retrieval of data is successful from the view, the model gets updated
        with the data. Lastly, the Indeed.com search url is requested and upon
        a successful request the results are displayed.

        """
        self.run_view()
        self.get_model_data()
        self.insert_model_data()
        self.request_page()
        self.display_search_results()

    def run_view(self):
        """Runs the mainloop of the view - displays the GUI for data input."""
        self.view.mainloop()

    def get_model_data(self):
        """Retrieves the users data via the IndeedAppView GUI; otherwise,
        exits the program (if user quits the GUI).

        """
        try:
            data = self.view.get_data()
        except AttributeError:
            sys.exit()
        else:
            self.model_data = data

    def insert_model_data(self):
        """Using the setter function provided by the model, data is updated
        according to the necessary parameters of city, state, search_terms, and
        num_results.

        """
        self.model.initialize_data(**self.model_data)

    def request_page(self):
        """Requests the URL that was formatted within the model. If successful,
        then the pages with display; otherwise, the program will exit.

        """
        self.model.request_page()

    def display_search_results(self):
        """Displays the desired number of results that was chosen by the user
        in the view GUI.

        """
        self.model.display_job_search_results()
