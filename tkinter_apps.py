#!/usr/bin/python3
import tkinter as tk

class GetLocGUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        master.title("Indeed.com Job Search App")
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.city_label = tk.Label(self, text="Input city name:")
        self.city_entry = tk.Entry(self, textvariable=self.getEntryFields)
        self.city_label.grid(row=0, column=0)
        self.city_entry.grid(row=0, column=1)

        self.state_label = tk.Label(self, text="Input state abbreviation:")
        self.state_entry = tk.Entry(self, textvariable=self.getEntryFields)
        self.state_label.grid(row=1, column=0)
        self.state_entry.grid(row=1, column=1)

        self.confirm_button = tk.Button(self, text="Confirm", \
                                       command=self.getEntryFields)
        self.confirm_button.grid(row=2, column=0)

        self.quit_button = tk.Button(self, text="Quit", command=self.quit)
        self.quit_button.grid(row=2, column=1)

    def getEntryFields(self):
        self.city = self.city_entry.get()
        self.state = self.state_entry.get()
        self.quit()

    def getLocation(self):
        return self.city, self.state


class GetSearchTermsGUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        master.title("Indeed.com Job Search App")
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        prompt = "Input search terms, separating each with commas:"
        self.search_terms_label = tk.Label(self, text=prompt)
        self.search_terms_entry = tk.Entry(self, \
                textvariable=self.getEntryField)
        self.search_terms_label.grid(row=0, column=0)
        self.search_terms_entry.grid(row=1, column=0)

        self.confirm_button = tk.Button(self, text="Confirm", \
                                       command=self.getEntryField)
        self.confirm_button.grid(row=2, column=0)

        self.quit_button = tk.Button(self, text="Quit", command=self.quit)
        self.quit_button.grid(row=2, column=1)

    def getEntryField(self):
        self.search_terms = self.search_terms_entry.get()
        self.quit()

    def getSearchTerms(self):
        return self.search_terms.split(sep = ",")


class GetNumResultsGUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        master.title("Indeed.com Job Search App")
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        prompt = "How many search results to display?"
        self.num_results_label = tk.Label(self, text=prompt)
        self.num_results_entry = tk.Entry(self, textvariable=self.getEntryField)
        self.num_results_label.grid(row=0, column=0)
        self.num_results_entry.grid(row=0, column=1)

        self.confirm_button = tk.Button(self, text="Confirm", \
                                       command=self.getEntryField)
        self.confirm_button.grid(row=1, column=0)

        self.quit_button = tk.Button(self, text="Quit", command=self.quit)
        self.quit_button.grid(row=1, column=1)

    def getEntryField(self):
        self.num_results = self.num_results_entry.get()
        self.quit()

    def getNumResults(self):
        return self.num_results


def main():
    location_root = tk.Tk()
    get_loc_app = GetLocGUI(master=location_root)
    get_loc_app.mainloop()
    city, state = get_loc_app.getLocation()
    location_root.destroy()

    search_terms_root = tk.Tk()
    get_st_app = GetSearchTermsGUI(master=search_terms_root)
    get_st_app.mainloop()
    search_terms = get_st_app.getSearchTerms()
    search_terms_root.destroy()

    num_results_root = tk.Tk()
    get_num_results_app = GetNumResultsGUI(master=num_results_root)
    get_num_results_app.mainloop()
    num_results = get_num_results_app.getNumResults()
    num_results_root.destroy()

    prompt = "The following data has been entered:\n"
    prompt += "Location: {city}, {state}\n"
    prompt += "Search Terms: {search_terms}\n"
    prompt += "Number of Results: {num_results}\n"
             
    print(prompt.format(city=city, state=state, \
            search_terms=search_terms, num_results=num_results))

if __name__ == "__main__":
    main()
