import tkinter as tk
from tkinter import ttk, messagebox
from feed_record import FeedRecord
from cow import show_all_cows
from datetime import datetime
import threading

class FeedRecordsApp(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Feed Records Management")
        self.geometry("800x600")

        # Feed record table on the left
        self.feed_record_frame = ttk.Frame(self)
        self.feed_record_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Form on the right
        self.form_frame = ttk.Frame(self, borderwidth=2, relief="groove", padding=(10, 10))
        self.form_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH)

        # Display the table and form
        self.show_feed_records()
        self.add_feed_record_form()

    def show_feed_records(self):
        # Table headers
        columns = ("ID", "Cow ID", "Feed Type", "Quantity", "Date")
        self.tree = ttk.Treeview(self.feed_record_frame, columns=columns, show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cow ID", text="Cow ID")
        self.tree.heading("Feed Type", text="Feed Type")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Date", text="Date")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Buttons for updating and deleting
        self.update_button = ttk.Button(self.feed_record_frame, text="Update", command=self.update_record)
        self.delete_button = ttk.Button(self.feed_record_frame, text="Delete", command=self.delete_record)
        self.update_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Initially load the data
        self.refresh_feed_records()

    def add_feed_record_form(self):
        # Title
        ttk.Label(self.form_frame, text="Add Feed Record", font=("Arial", 14)).pack(pady=10)

        # Dropdown for cows
        cows = show_all_cows()
        self.cow_var = tk.StringVar()
        cow_options = {str(cow.id): cow.name for cow in cows}  # Store cow ID and name
        self.cow_menu = ttk.Combobox(self.form_frame, textvariable=self.cow_var, values=[f"{cow.id} - {cow.name}" for cow in cows])
        self.cow_menu.pack(pady=5)

        # Feed type field
        ttk.Label(self.form_frame, text="Feed Type").pack(pady=5)
        self.feed_type_entry = ttk.Entry(self.form_frame)
        self.feed_type_entry.pack(pady=5)

        # Quantity field
        ttk.Label(self.form_frame, text="Quantity").pack(pady=5)
        self.quantity_entry = ttk.Entry(self.form_frame)
        self.quantity_entry.pack(pady=5)

        # Date field
        ttk.Label(self.form_frame, text="Date (YYYY-MM-DD)").pack(pady=5)
        self.date_entry = ttk.Entry(self.form_frame)
        self.date_entry.pack(pady=5)

        # Submit button
        self.submit_button = ttk.Button(self.form_frame, text="Add Feed Record", command=self.submit_feed_record)
        self.submit_button.pack(pady=10)

    def submit_feed_record(self):
        # Extract cow ID from selected value
        selected_cow = self.cow_menu.get()
        if not selected_cow:
            messagebox.showerror("Error", "Please select a cow.", parent=self)
            return

        # Extract only the cow ID (ensure it's an integer)
        cow_id = selected_cow.split(" - ")[0]  # Extract only the cow ID (assumed to be in the format 'ID - Name')
        if not cow_id.isdigit():
            messagebox.showerror("Error", "Invalid cow ID.", parent=self)
            return

        cow_id = int(cow_id)  # Convert cow_id to integer

        feed_type = self.feed_type_entry.get()
        quantity = self.quantity_entry.get()
        record_date = self.date_entry.get()

        try:
            record_date = datetime.strptime(record_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.", parent=self)
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity.", parent=self)
            return

        # Run the record insertion in a separate thread
        self.add_feed_record_in_background(cow_id, feed_type, quantity, record_date)

    def add_feed_record_in_background(self, cow_id, feed_type, quantity, record_date):
        # Use threading to avoid blocking the main thread
        def task():
            result = FeedRecord.add_feed_record(cow_id, feed_type, quantity, record_date)
            if result == 'success':
                # Ensure the UI is updated from the main thread using Tkinter's after() method
                self.after(0, lambda: self.on_feed_record_added())
            else:
                self.after(0, lambda: messagebox.showerror("Error", "Failed to add feed record.", parent=self))

        threading.Thread(target=task).start()

    def on_feed_record_added(self):
        """Called after a record is added to refresh the UI."""
        self.refresh_feed_records()
        messagebox.showinfo("Success", "Feed record added successfully!", parent=self)

    def refresh_feed_records(self):
        # Clear the table before inserting updated records
        self.tree.delete(*self.tree.get_children())

        # Fetch updated feed records
        all_feed_records = FeedRecord.show_all_feed_records()

        # Insert updated records
        for record in all_feed_records:
            self.tree.insert("", tk.END, values=(record.id, record.cow_id, record.feed_type, record.quantity, record.date))

    def delete_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            record_id = self.tree.item(selected_item)["values"][0]
            result = FeedRecord.delete_feed_record(record_id)
            if result == 'success':
                self.refresh_feed_records()
                messagebox.showinfo("Success", "Record deleted successfully!", parent=self)
            else:
                messagebox.showerror("Error", "Failed to delete record.", parent=self)
        else:
            messagebox.showerror("Error", "Please select a record to delete.", parent=self)

    def update_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            record_id = self.tree.item(selected_item)["values"][0]
            feed_type = self.feed_type_entry.get()
            quantity = self.quantity_entry.get()

            if feed_type and quantity:
                try:
                    quantity = int(quantity)
                    result = FeedRecord.update_feed_record(record_id, feed_type, quantity)
                    if result == 'success':
                        self.refresh_feed_records()
                        messagebox.showinfo("Success", "Record updated successfully!", parent=self)
                    else:
                        messagebox.showerror("Error", "Failed to update record.", parent=self)
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid quantity.", parent=self)
            else:
                messagebox.showerror("Error", "Please enter feed type and quantity to update.", parent=self)
        else:
            messagebox.showerror("Error", "Please select a record to update.", parent=self)
