#!/usr/bin/python3
import tkinter as tk

class GetDataApp(tk.Frame):
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

        prompt = "Input search terms, separating each with commas:"
        self.search_terms_label = tk.Label(self, text=prompt)
        self.search_terms_entry = tk.Entry(self, \
                textvariable=self.getEntryFields)
        self.search_terms_label.grid(row=2, column=0)
        self.search_terms_entry.grid(row=2, column=1)

        prompt = "How many search results to display?"
        self.num_results_label = tk.Label(self, text=prompt)
        self.num_results_entry = tk.Entry(self, \
                textvariable=self.getEntryFields)
        self.num_results_label.grid(row=3, column=0)
        self.num_results_entry.grid(row=3, column=1)

        self.confirm_button = tk.Button(self, text="Confirm", \
                                       command=self.getEntryFields)
        self.confirm_button.grid(row=4, column=0)

        self.quit_button = tk.Button(self, text="Quit", command=self.quit)
        self.quit_button.grid(row=4, column=1)

    def getEntryFields(self):
        self.city = self.city_entry.get()
        self.state = self.state_entry.get()
        self.search_terms = self.search_terms_entry.get()
        self.num_results = self.num_results_entry.get()
        self.quit()

    def getData(self):
        """Returns the data provided from the app in a dictionary."""
        data = {"city": self.city.strip(),
                "state": self.state.strip(),
                "search_terms": [term.strip() for term in \
                        self.search_terms.split(sep = ",")],
                "num_results": self.num_results}
        return data


def main():
    app_root = tk.Tk()
    get_data_app = GetDataApp(master=app_root)
    get_data_app.mainloop()
    data = get_data_app.getData()
    app_root.destroy()

    prompt = "The following data has been entered:\n"
    prompt += "Location: {city}, {state}\n"
    prompt += "Search Terms: {search_terms}\n"
    prompt += "Number of Results: {num_results}\n"
             
    print(prompt.format(**data))

if __name__ == "__main__":
    main()
