#!/usr/bin/python3

import sys
from model import IndeedAppModel
from view import IndeedAppView

class IndeedAppController(object):

    def __init__(self):
        self.model = IndeedAppModel()
        self.view = IndeedAppView()

    def start_app(self):
        self.run_view()
        self.get_model_data()
        self.insert_model_data()
        self.request_page()
        self.display_search_results()

    def run_view(self):
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
        self.model.initialize_data(**self.model_data)

    def request_page(self):
        self.model.request_page()

    def display_search_results(self):
        self.model.display_job_search_results()
