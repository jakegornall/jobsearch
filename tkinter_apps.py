#!/usr/bin/python3
import csv
import tkinter as tk
from tkinter import messagebox

class GetDataApp(tk.Frame):
    def __init__(self, root, state_abbrs):
        tk.Frame.__init__(self, root)
        self.root = root
        self.state_abbrs = state_abbrs

        self._initializeWidgets()
        self._setWidgets()

    def _initializeWidgets(self):
        loc_frame = tk.Frame(self.root)
        loc_prompts = ["Input city name:", "Select state abbreviation:"]
        self.city_label = tk.Label(loc_frame, text=loc_prompts[0])
        self.city_entry = tk.Entry(loc_frame)

        self.state_label = tk.Label(loc_frame, text=loc_prompts[1])
        self.state_lbox = tk.Listbox(loc_frame, height=6, justify=tk.CENTER)
        for state in self.state_abbrs:
            self.state_lbox.insert(tk.END, state)

        terms_frame = tk.Frame(self.root)
        prompt = "Input search terms:\n(separate with commas)"
        self.search_terms_label = tk.Label(terms_frame, text=prompt)
        self.search_terms_entry = tk.Entry(terms_frame)

        results_frame = tk.Frame(self.root)
        prompt = "How many search results to display? (Check one)"
        self.num_results_label = tk.Label(results_frame, text=prompt)

        self.num_results_vars = [tk.IntVar() for _ in range(3, 11)]
        self.num_results_chkbtns = []
        for i in range(3, 11):
            self.num_results_chkbtns.append(tk.Checkbutton(results_frame, \
                    text=i, variable=self.num_results_vars[i-3]))

        bottom_frame = tk.Frame(self.root)
        self.confirm_button = tk.Button(bottom_frame, text="Confirm", \
                command=self._extractEntryFields)
        self.quit_button = tk.Button(bottom_frame, text="Quit", \
                command=self.quit)

    def _setWidgets(self):
        loc_frame.pack()
        self.city_label.pack()
        self.city_entry.pack()
        self.state_label.pack()
        self.state_lbox.pack()

        terms_frame.pack()
        self.search_terms_label.pack(side=tk.LEFT)
        self.search_terms_entry.pack(side=tk.LEFT)

        results_frame.pack()
        self.num_results_label.pack(side=tk.TOP)
        for num_results_chkbtn in self.num_results_chkbtns:
            num_results_chkbtn.pack(side=tk.LEFT)

        bottom_frame.pack()
        self.confirm_button.pack(side=tk.LEFT)
        self.quit_button.pack(side=tk.LEFT)

    def _verifyNumResults(self):
        """Checks if only one button is selected."""
        check = 0
        for chkbtn in self.num_results_vars:
            value = chkbtn.get()
            check += value
        if check == 1:
            return True
        return False

    def _getNumResults(self):
        """Returns the number of results."""
        check_btns_vals = [chkbtn.get() for chkbtn in self.num_results_vars]
        num_results_idx = check_btns_vals.index(max(check_btns_vals))
        num_results = num_results_idx + 3  # Because user given choice of 3-10
        return num_results

    def _extractEntryFields(self):
        """Retrieves the input data from the entry fields in the app."""
        if self._verifyNumResults():
            self.city = self.city_entry.get()

            state_idx = self.state_lbox.curselection()
            self.state = self.state_lbox.get(self.state_lbox.curselection())

            self.search_terms = self.search_terms_entry.get()
            self.num_results = self._getNumResults()
            self.quit()
        else:
            msg = "Check only one box for\nthe number of results."
            messagebox.showinfo("Indeed.com Job Search", msg)

    def getData(self):
        """Creates a dictionary of the data provided from the app.

        Returns
        =======
        data_dict (dict) : Dictionary with keywords corresponding to each of
                the entry fields, along with the corresponding data entered.

        """
        data_dict = {"city": self.city.strip(),
                    "state": self.state.strip(),
                    "search_terms": [term.strip() for term in \
                        self.search_terms.split(sep = ",")],
                    "num_results": self.num_results}
        return data_dict


def getStateAbbr(state_abbr_file):
    """Reads the state abbreviations from a text file given by the input.

    Parameters
    ==========
    state_abbr_file (str) : String corresponding to the text file with the
            state abbreviations.

    Returns
    =======
    state_abbrs (list) : List of strings with each state abbreviation.

    """
    state_abbrs = []
    with open(state_abbr_file) as f_obj:
        reader = csv.reader(f_obj)
        for row in reader:
            state_abbrs.append(row[0])
    return state_abbrs

def displayData(data_dict):
    """Displays the inputted data via tk.messagebox to the user.

    Parameters
    ==========
    data_dict (dict) : Contains the city, state, search_term list and number of
        search results via keywords in a dictionary.

    """
    msg = "You have entered:\n"
    msg += "Location: {city}, {state}\n"
    msg += "Search Terms: {search_terms}\n"
    msg += "Number of Results: {num_results}\n"
    messagebox.showinfo("Indeed.com Job Search", msg.format(**data_dict))

def main():
    app_root = tk.Tk()
    app_root.title("Indeed.com Job Search App")
    state_abbrs = getStateAbbr("postal_codes.txt")
    get_data_app = GetDataApp(app_root, state_abbrs)
    get_data_app.mainloop()
    data_dict = get_data_app.getData()

    displayData(data_dict)


if __name__ == "__main__":
    main()
