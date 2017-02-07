#!/usr/bin/python3

"""
                    App for Collecting User Data for Indeed.com
    Author: Zach Churchill
    Python Version: 3.5.2
    Description: The app displays a form to the user with the following fields:
        city, state, search terms, and number of results. Both the city and
        search terms require the user to fill in information via the keyboard,
        and user input is not validated in that the user can enter whatever
        is desired. The state field is a list box that allows the user to choose
        the corresponding state abbreviation for their location. Lastly, the
        number of search terms is a set of radio buttons that, by default, only
        allow the user to fill in one.
        An important feature of the app is that the user must fill in/select
        an option from each field in order to continue; that is, the app does
        not allow the user to leave fields blank/unchecked.
"""

from controller import IndeedAppController

def main():
    app_controller = IndeedAppController()
    app_controller.start_app()

if __name__ == "__main__":
    main()
