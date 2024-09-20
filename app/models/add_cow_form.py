import tkinter as tk
from tkinter import ttk, messagebox
from cow import Cow, show_all_cows
from datetime import datetime

def open_add_cow_form():
    # Create a new top-level window for the cow form
    new_window = tk.Toplevel()
    new_window.title('Manage Cow Records')
    new_window.geometry('1000x500')

    # Configure ttk styles
    style = ttk.Style()
    style.configure('TLabel', font=('Arial', 12), foreground='black')
    style.configure('TEntry', font=('Arial', 14), padding=8, foreground='black')
    style.configure('TButton', font=('Arial', 12), padding=10)

    # Frame for cow table on the left
    cow_table_frame = ttk.Frame(new_window, padding=10, borderwidth=2, relief="solid")
    cow_table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Frame for the cow form on the right
    cow_form_frame = ttk.Frame(new_window, padding=10, borderwidth=2, relief="solid")
    cow_form_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Title for cow form
    title_label = ttk.Label(cow_form_frame, text='Add New Cow', font=('Arial', 20, 'bold'))
    title_label.grid(row=0, column=0, columnspan=2, pady=20)

    # Cow name input
    cow_name_label = ttk.Label(cow_form_frame, text='Cow Name:', style='TLabel')
    cow_name_entry = ttk.Entry(cow_form_frame, width=30)
    cow_name_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
    cow_name_entry.grid(row=1, column=1, padx=20, pady=10)

    # Cow tag input
    cow_tag_label = ttk.Label(cow_form_frame, text='Cow Tag:', style='TLabel')
    cow_tag_entry = ttk.Entry(cow_form_frame, width=30)
    cow_tag_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
    cow_tag_entry.grid(row=2, column=1, padx=20, pady=10)

    # Birthdate input
    cow_birthdate_label = ttk.Label(cow_form_frame, text='Birthdate (YYYY-MM-DD):', style='TLabel')
    cow_birthdate_entry = ttk.Entry(cow_form_frame, width=30)
    cow_birthdate_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
    cow_birthdate_entry.grid(row=3, column=1, padx=20, pady=10)

    # Breed input
    cow_breed_label = ttk.Label(cow_form_frame, text='Cow Breed:', style='TLabel')
    cow_breed_entry = ttk.Entry(cow_form_frame, width=30)
    cow_breed_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
    cow_breed_entry.grid(row=4, column=1, padx=20, pady=10)

    # Submit button for adding cow
    def submit_cow_form():
        if cow_name_entry.get() == '' or cow_tag_entry.get() == '' or cow_birthdate_entry.get() == '' or cow_breed_entry.get() == '':
            messagebox.showerror("Error", "You left a field empty, make sure all fields are filled", parent=new_window)
        else:
            new_cow = Cow(
                name=cow_name_entry.get(),
                breed=cow_breed_entry.get(),
                birth_date=datetime.strptime(cow_birthdate_entry.get(), "%Y-%m-%d"),
                tag_number=cow_tag_entry.get()
            )
            new_cow.add_cows()
            messagebox.showinfo("Success", "Cow record added successfully", parent=new_window)
            refresh_cow_list()  # Refresh the cow list after adding
            # Clear the form fields
            cow_name_entry.delete(0, tk.END)
            cow_tag_entry.delete(0, tk.END)
            cow_birthdate_entry.delete(0, tk.END)
            cow_breed_entry.delete(0, tk.END)

    submit_button = ttk.Button(cow_form_frame, text='Add Cow', command=submit_cow_form)
    submit_button.grid(row=5, column=0, columnspan=2, pady=20)

    # Table to display cows (on the left side)
    columns = ('Name', 'Tag', 'Birthdate', 'Breed')
    cow_table = ttk.Treeview(cow_table_frame, columns=columns, show='headings')
    cow_table.heading('Name', text='Name')
    cow_table.heading('Tag', text='Tag')
    cow_table.heading('Birthdate', text='Birthdate')
    cow_table.heading('Breed', text='Breed')

    # Scrollbar for the table
    cow_table_scrollbar = ttk.Scrollbar(cow_table_frame, orient="vertical", command=cow_table.yview)
    cow_table.configure(yscroll=cow_table_scrollbar.set)
    cow_table_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Table actions: Update and Delete
    def delete_cow_handler(cow_id):
        cow = Cow.get_cow_by_id(cow_id)
        if messagebox.askyesno('Confirm Delete', f"Are you sure you want to delete {cow.name}?", parent=new_window):
            cow.delete_cows()
            refresh_cow_list()

    def update_cow_handler(cow_id):
        cow = Cow.get_cow_by_id(cow_id)
        cow_name_entry.delete(0, tk.END)
        cow_tag_entry.delete(0, tk.END)
        cow_birthdate_entry.delete(0, tk.END)
        cow_breed_entry.delete(0, tk.END)

        cow_name_entry.insert(0, cow.name)
        cow_tag_entry.insert(0, cow.tag_number)
        cow_birthdate_entry.insert(0, cow.birth_date.strftime("%Y-%m-%d"))
        cow_breed_entry.insert(0, cow.breed)

        def save_updated_cow():
            cow.name = cow_name_entry.get()
            cow.tag_number = cow_tag_entry.get()
            cow.birth_date = datetime.strptime(cow_birthdate_entry.get(), "%Y-%m-%d")
            cow.breed = cow_breed_entry.get()
            cow.update_cow()  # Update the cow record
            messagebox.showinfo("Success", "Cow record updated successfully", parent=new_window)
            refresh_cow_list()
            submit_button.config(text='Add Cow', command=submit_cow_form)

        submit_button.config(text='Save Changes', command=save_updated_cow)

    def refresh_cow_list():
        # Clear the current items in the cow table
        for row in cow_table.get_children():
            cow_table.delete(row)

        # Fetch and display cows in the table
        all_cows = show_all_cows()
        for cow in all_cows:
            cow_table.insert('', 'end', values=(cow.name, cow.tag_number, cow.birth_date, cow.breed))

    # Add button controls for selected rows
    def on_row_selected(event):
        selected_item = cow_table.selection()  # Get selected row
        if selected_item:
            cow_id = cow_table.item(selected_item)['values'][1]  # Assume cow_id is the Tag (second column)
            delete_button.config(command=lambda: delete_cow_handler(cow_id))
            update_button.config(command=lambda: update_cow_handler(cow_id))

    # Bind the row selection event
    cow_table.bind('<<TreeviewSelect>>', on_row_selected)

    # Pack the table
    cow_table.pack(fill=tk.BOTH, expand=True)

    # Delete and Update Buttons
    delete_button = ttk.Button(new_window, text="Delete Cow", state=tk.DISABLED)  # Initially disabled
    delete_button.pack(side=tk.LEFT, padx=10, pady=10)

    update_button = ttk.Button(new_window, text="Update Cow", state=tk.DISABLED)  # Initially disabled
    update_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # Enable buttons when row is selected
    cow_table.bind('<<TreeviewSelect>>', lambda e: [delete_button.config(state=tk.NORMAL), update_button.config(state=tk.NORMAL)])

    # Initial load of cow data
    refresh_cow_list()
