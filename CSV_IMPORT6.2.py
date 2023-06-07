import requests
import json
import time
import csv
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import threading

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("CSV Importer for Personal AI")
        self.geometry("700x500")

        self.create_widgets()
        self.importing = threading.Event()

    def create_widgets(self):
        self.profile_label = tk.Label(self, text="AI DomainName:")
        self.profile_entry = tk.Entry(self, width=50)

        self.profile_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.profile_entry.grid(row=2, column=1, padx=10, pady=10)

        self.api_key_label = tk.Label(self, text="API Key:")
        self.api_key_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.api_key_entry = tk.Entry(self, width=50)
        self.api_key_entry.grid(row=3, column=1, padx=10, pady=10)

        self.source_name_label = tk.Label(self, text="Source Name:")
        self.source_name_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

        self.source_name_entry = tk.Entry(self, width=50)
        self.source_name_entry.grid(row=4, column=1, padx=10, pady=10)

        self.created_time_label = tk.Label(self, text="Created Time:")
        self.created_time_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        self.created_time_entry = tk.Entry(self, width=50)
        self.created_time_entry.grid(row=5, column=1, padx=10, pady=10)

        self.device_name_label = tk.Label(self, text="Device Name:")
        self.device_name_label.grid(row=6, column=0, padx=10, pady=10, sticky="e")

        self.device_name_entry = tk.Entry(self, width=50)
        self.device_name_entry.grid(row=6, column=1, padx=10, pady=10)

        self.file_label = tk.Label(self, text="File:")
        self.file_entry = tk.Entry(self, width=50)

        self.file_label.grid(row=7, column=0, padx=10, pady=10, sticky="e")
        self.file_entry.grid(row=7, column=1, padx=10, pady=10)

        self.import_button = tk.Button(self, text="Submit CSV", command=self.import_csv)
        self.import_button.grid(row=8, column=2, padx=10, pady=10)

        self.status_label = tk.Label(self, text="")
        self.status_label.grid(row=9, column=1, padx=10, pady=10)  # Moved to a new row

        self.submitted_data_label = tk.Label(self, text="Submitted Data:")
        self.submitted_data_label.grid(row=10, column=0, padx=10, pady=10, sticky="e")

        self.submitted_data_text = tk.Text(self, width=50, height=5)
        self.submitted_data_text.grid(row=10, column=1, padx=10, pady=10)

        self.exit_button = tk.Button(self, text="Exit", command=self.terminate_import)
        self.exit_button.grid(row=11, column=1, padx=10, pady=10)  # Adjusted the row


    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

        if not file_path:
            return

        self.file_entry.delete(0, 'end')
        self.file_entry.insert(0, file_path)

        self.status_label.config(text="Wait...")
        self.update_idletasks()

        with open(file_path, newline='', encoding='utf-8', errors='ignore') as csvfile:
            reader = csv.reader(x.replace('\0', '') for x in csvfile)
            for row in reader:
                if not self.importing:
                    break
                if not row or all(cell == '' for cell in row):
                    continue
                self.process_row(row)
            time.sleep(1)

        self.status_label.config(text="Completed")

    def terminate_import(self):
        self.importing.clear()
        self.quit()

    def process_row(self, row):
        base_url = 'https://api.personal.ai/v1'

        api_key = self.api_key_entry.get()
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
        }

        data = ' '.join(row)
        self.upload_data_to_ai_memory (data, base_url, headers)

    def upload_data_to_ai_memory(self, data, base_url, headers):
        memory_url = f'{base_url}/memory'
        current_time = self.created_time_entry.get() or datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        source_name = self.source_name_entry.get()
        domain_name = self.profile_entry.get()
        device_name = self.device_name_entry.get()
        memory_object = {
            "Text": data,
            "SourceName": source_name,
            "CreatedTime": current_time,
            "DomainName": domain_name,
            "DeviceName": device_name,
        }
        # Update the submitted data text widget
        self.submitted_data_text.insert(tk.END, f'{data}\n')
        self.submitted_data_text.see(tk.END)
        self.update_idletasks()

        response = requests.post(url=memory_url, headers=headers, json=memory_object)

        if response.status_code != 200:
            print("Error uploading data:", response.status_code)
            print(response.text)

if __name__ == "__main__":
    app = Application()
    app.mainloop()


