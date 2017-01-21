#!/usr/bin/python3
import csv
import tkinter as tk
from tkinter import messagebox as msgBox


class GetDataApp(tk.Frame):
    STATE_ABBR_FILE = "postal_codes.txt"

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.state_abbrs = GetDataApp.getStateAbbr()

        self._setAppWindow()
        self._initializeWidgets()
        self._setWidgets()

    def _getStateAbbr(state_abbr_file):
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
        with open(GetDataApp.STATE_ABBR_FILE) as f_obj:
            reader = csv.reader(f_obj)
            for row in reader:
                state_abbrs.append(row[0])
        return state_abbrs

    def _setAppWindow(self):
        """Sets the features of the app window."""
        self.root.title("Indeed.com Job Search App")
        self.root.resizable(0,0)

    def _initializeWidgets(self):
        """Creates and initializes all of the necessary widgets with text,
        commands, and key bindings.

        """
        self.loc_frame = tk.Frame(self.root)
        loc_prompts = ["Input city name:", "Select state abbreviation:"]
        self.city_label = tk.Label(self.loc_frame, text=loc_prompts[0])
        self.city_entry = tk.Entry(self.loc_frame)
        self.state_label = tk.Label(self.loc_frame, text=loc_prompts[1])
        self.state_scrollbar = tk.Scrollbar(
                                    self.loc_frame,
                                    orient=tk.VERTICAL,
                                    command=self._onMousewheel)
        self.state_lbox = tk.Listbox(
                                self.loc_frame,
                                yscrollcommand=self.state_scrollbar.set,
                                height=6,
                                justify=tk.CENTER
                                )
        for state in self.state_abbrs:
            self.state_lbox.insert(tk.END, state)
        self.state_lbox.bind("<<ListboxSelect>>", self._onSelect)
        self.state_scrollbar.config(command=self.state_lbox.yview)

        self.state_selected_frame = tk.Frame(self.root)
        self.state_selected_lbl = tk.Label(
                                        self.state_selected_frame,
                                        text="State Selected:"
                                        )
        self.state_selected_var = tk.StringVar()
        self.state_selected_var.set("")
        self.state_selected = tk.Label(
                                    self.state_selected_frame,
                                    textvariable=self.state_selected_var
                                    )

        self.terms_frame = tk.Frame(self.root)
        prompt = "Input search terms:\n(separate with commas)"
        self.search_terms_label = tk.Label(self.terms_frame, text=prompt)
        self.search_terms_entry = tk.Entry(self.terms_frame)

        self.num_results_frame = tk.Frame(self.root)
        prompt = "How many search results to display?"
        self.num_results_label = tk.Label(self.num_results_frame, text=prompt)
        self.num_results_radio_btns = []
        self.num_results_radio_var = tk.IntVar()
        for i in range(3, 11):
            radio_btn = tk.Radiobutton(
                                self.num_results_frame,
                                text=i,
                                variable=self.num_results_radio_var,
                                value=i
                                )
            self.num_results_radio_btns.append(radio_btn)

        self.btns_frame = tk.Frame(self.root)
        self.confirm_button = tk.Button(
                                    self.btns_frame,
                                    text="Confirm",
                                    command=self._extractEntryFields
                                    )
        self.confirm_button.bind("<Return>", self._extractEntryFields)
        self.quit_button = tk.Button(
                                self.btns_frame,
                                text="Quit",
                                command=self._exitApp
                                )
        self.quit_button.bind("<Return>", self._exitApp)

    def _setWidgets(self):
        """Packs the widgets according my personal app design."""
        self.loc_frame.pack()
        self.city_label.pack()
        self.city_entry.pack()
        self.state_label.pack()
        self.state_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.state_lbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.state_selected_frame.pack()
        self.state_selected_lbl.pack(side=tk.LEFT)
        self.state_selected.pack(side=tk.RIGHT)

        self.terms_frame.pack()
        self.search_terms_label.pack(side=tk.LEFT)
        self.search_terms_entry.pack(side=tk.LEFT)

        self.num_results_frame.pack()
        self.num_results_label.pack()
        for radio_btn in self.num_results_radio_btns:
            radio_btn.pack(side=tk.LEFT)

        self.btns_frame.pack()
        self.confirm_button.pack(side=tk.LEFT)
        self.quit_button.pack(side=tk.LEFT)

    def _onSelect(self, *event):
        """Updates the state selected variable to the choice that the user
        stops at when selecting the state in the listbox widget.

        Parameters
        ==========
        event (tk.Event) : Optional parameter provided for buttons that have
            a key stroke binded to them.

        """
        widget = event.widget
        try:
            index = int(widget.curselection()[0])
        except IndexError:
            pass
        else:
            value = widget.get(index)
            self.state_selected_var.set(value)

    def _onMousewheel(self, *event):
        """Allows the mousewheel to be used for scrolling in widgets.

        Parameters
        ==========
        event (tk.Event) : Optional parameter provided for buttons that have
            a key stroke binded to them.

        """
        self.root.yview_scroll(-1*(event.delta/120), "units")

    def _extractSearchTerms(self):
        """Extracts and strips the search terms of whitespace on both sides.

        Returns
        =======
        search_terms (list) : List of strings containing the entered terms.

        """
        input_terms = self.search_terms_entry.get()
        search_terms = [term.strip() for term in input_terms.split(sep = ",")]
        return search_terms

    def _extractEntryFields(self, *event):
        """If all of the data has been enter, the data is retrieved the from
        the entry fields in the app and stores in a dictionary, then exits app
        after data retrieval; otherwise, if all of the data isn't filled in
        then a message box appears instructing the user to fill in the fields.

        Parameters
        ==========
        event (tk.Event) : Optional parameter provided for buttons that have
            a key stroke binded to them.

        """
        city = self.city_entry.get().strip()
        state = self.state_selected_var.get()
        search_terms = self._extractSearchTerms()
        num_results = self.num_results_radio_var.get()

        if city and state and search_terms and num_results:
            self.data_dict = {"city": city,
                             "state": state,
                             "search_terms": search_terms,
                             "num_results": num_results
                             }
            self._exitApp()
        else:
            error_msg = "Fill in all of the fields."
            self._showErrorMsgBox(error_msg)

    def _exitApp(self, *event):
        """Uses the quit method of tk.Tk() to close the application interface.

        Parameters
        ==========
        event (tk.Event) : Optional parameter provided for buttons that have
            a key stroke binded to them.

        """
        self.root.quit()

    def _showErrorMsgBox(self, error_msg):
        """Creates a message box with the given error text to print to the
        screen.

        Parameters
        ==========
        error_msg (str) : String containing the error message to user.

        """
        msgBox.showinfo("ERROR", error_msg)

    def getData(self):
        """Creates a dictionary of the data provided from the app.

        Returns
        =======
        data_dict (dict) : Dictionary with keywords corresponding to each of
                the entry fields, along with the corresponding data entered.

        """
        return self.data_dict


def main():
    app_root = tk.Tk()
    get_data_app = GetDataApp(app_root)
    get_data_app.mainloop()

if __name__ == "__main__":
    main()
