import tkinter as tk
from tkinter import ttk, messagebox
from milk_record import MilkRecord
from cow import show_all_cows
from datetime import datetime
import threading

class MilkRecordsApp(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Milk Records Management")
        self.geometry("800x600")

        # Milk record table on the left
        self.milk_record_frame = ttk.Frame(self)
        self.milk_record_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Form on the right
        self.form_frame = ttk.Frame(self, borderwidth=2, relief="groove", padding=(10, 10))
        self.form_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH)

        # Display and form methods
        self.show_milk_records()
        self.add_milk_record_form()

    def show_milk_records(self):
        # Table headers
        columns = ("ID", "Cow ID", "Date", "Milk Quantity")
        self.tree = ttk.Treeview(self.milk_record_frame, columns=columns, show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cow ID", text="Cow ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Milk Quantity", text="Milk Quantity")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Buttons for updating and deleting
        self.update_button = ttk.Button(self.milk_record_frame, text="Update", command=self.update_record)
        self.delete_button = ttk.Button(self.milk_record_frame, text="Delete", command=self.delete_record)
        self.update_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Initially load the data
        self.refresh_milk_records()

    def add_milk_record_form(self):
        # Title
        ttk.Label(self.form_frame, text="Add Milk Record", font=("Arial", 14)).pack(pady=10)

        # Dropdown for cows
        cows = show_all_cows()
        self.cow_var = tk.StringVar()
        cow_options = {str(cow.id): cow.name for cow in cows}  # Store cow ID and name
        self.cow_menu = ttk.Combobox(self.form_frame, textvariable=self.cow_var, values=[f"{cow.id} - {cow.name}" for cow in cows])
        self.cow_menu.pack(pady=5)

        # Date field
        ttk.Label(self.form_frame, text="Date (YYYY-MM-DD)").pack(pady=5)
        self.date_entry = ttk.Entry(self.form_frame)
        self.date_entry.pack(pady=5)

        # Milk quantity
        ttk.Label(self.form_frame, text="Milk Quantity").pack(pady=5)
        self.quantity_entry = ttk.Entry(self.form_frame)
        self.quantity_entry.pack(pady=5)

        # Submit button
        self.submit_button = ttk.Button(self.form_frame, text="Add Milk Record", command=self.submit_milk_record)
        self.submit_button.pack(pady=10)

    def submit_milk_record(self):
        # Extract cow ID from selected value
        selected_cow = self.cow_menu.get()
        if not selected_cow:
            messagebox.showerror("Error", "Please select a cow.", parent=self)  # Added parent=self
            return

        cow_id = selected_cow.split(" - ")[0]  # Extract only the cow ID
        record_date = self.date_entry.get()
        milk_quantity = self.quantity_entry.get()

        try:
            record_date = datetime.strptime(record_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.", parent=self)  # Added parent=self
            return

        try:
            milk_quantity = float(milk_quantity)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid milk quantity.", parent=self)  # Added parent=self
            return

        # Run the record insertion in a separate thread
        self.add_milk_record_in_background(cow_id, record_date, milk_quantity)

    def add_milk_record_in_background(self, cow_id, record_date, milk_quantity):
        # Use threading to avoid blocking the main thread
        def task():
            result = MilkRecord.add_milk_record(cow_id, record_date, milk_quantity)
            if result == 'success':
                self.refresh_milk_records()
                messagebox.showinfo("Success", "Milk record added successfully!", parent=self)  # Added parent=self
            else:
                messagebox.showerror("Error", "Failed to add milk record.", parent=self)  # Added parent=self

        threading.Thread(target=task).start()

    def refresh_milk_records(self):
        # Clear the table before inserting updated records
        self.tree.delete(*self.tree.get_children())

        # Fetch updated milk records
        all_milk_records = MilkRecord.show_all_milk_records()

        # Insert updated records
        for record in all_milk_records:
            self.tree.insert("", tk.END, values=(record.id, record.cow_id, record.record_date, record.milk_quantity))

    def delete_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            record_id = self.tree.item(selected_item)["values"][0]
            result = MilkRecord.delete_milk_record(record_id)
            if result == 'success':
                messagebox.showinfo("Success", "Record deleted successfully!", parent=self)  # Added parent=self
                self.refresh_milk_records()
            else:
                messagebox.showerror("Error", "Failed to delete record.", parent=self)  # Added parent=self
        else:
            messagebox.showerror("Error", "Please select a record to delete.", parent=self)  # Added parent=self

    def update_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            record_id = self.tree.item(selected_item)["values"][0]
            new_quantity = self.quantity_entry.get()

            if new_quantity:
                try:
                    new_quantity = float(new_quantity)
                    result = MilkRecord.update_milk_record(record_id, new_quantity)
                    if result == 'success':
                        messagebox.showinfo("Success", "Record updated successfully!", parent=self)  # Added parent=self
                        self.refresh_milk_records()
                    else:
                        messagebox.showerror("Error", "Failed to update record.", parent=self)  # Added parent=self
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid milk quantity.", parent=self)  # Added parent=self
            else:
                messagebox.showerror("Error", "Please enter a new milk quantity to update.", parent=self)  # Added parent=self
        else:
            messagebox.showerror("Error", "Please select a record to update.", parent=self)  # Added parent=self
