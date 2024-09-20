import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from cow import show_all_cows, delete_cow
from milk_records_tk import MilkRecordsApp
from feed_record import FeedRecord
from milk_record import MilkRecord
from datetime import datetime, timedelta

# Placeholder for functions that open additional pages
from add_cow_form import open_add_cow_form
from feed_record_tk import FeedRecordsApp

def open_feed_records():
    FeedRecordsApp()

def open_add_cow():
    open_add_cow_form()
    refresh_cow_list()

def open_milk_records():
    MilkRecordsApp()

def delete_cow_handler(cow_id):
    delete = delete_cow(cow_id)
    if delete == 'success':
        messagebox.showinfo('Success', 'Cow record deleted successfully!')
        refresh_cow_list()
    else:
        messagebox.showerror('Error', 'Cow record not deleted.')

def refresh_cow_list():
    for widget in all_cows_table.get_children():
        all_cows_table.delete(widget)

    all_cows = show_all_cows()

    for cow in all_cows:
        all_cows_table.insert('', 'end', values=(cow.name, cow.breed))

def create_milk_graph():
    cows = show_all_cows()
    cow_names = [cow.name for cow in cows]

    # Retrieve milk production data
    milk_records = MilkRecord.show_all_milk_records()
    milk_data = {cow.id: 0 for cow in cows}

    for record in milk_records:
        milk_data[record.cow_id] += record.milk_quantity

    milk_quantities = [milk_data[cow.id] for cow in cows]

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(cow_names, milk_quantities, color="blue")
    ax.set_title("Total Milk Production Comparison")
    ax.set_ylabel("Milk Quantity (Liters)")

    return fig

def show_feed_records():
    for widget in feed_records_table.get_children():
        feed_records_table.delete(widget)

    # Get the last 25 feed records
    feed_records = FeedRecord.show_all_feed_records()[-25:]
    all_cows = {cow.id: cow.name for cow in show_all_cows()}  # Create a dictionary mapping cow_id to cow_name

    for record in feed_records:
        cow_name = all_cows.get(record.cow_id, "Unknown Cow")  # Safely get the cow name by cow_id
        feed_records_table.insert('', 'end', values=(cow_name, record.feed_type, record.quantity, record.date))
def show_weekly_monthly_production():
    # Fetch cows and milk records
    all_cows = show_all_cows()
    milk_records = MilkRecord.show_all_milk_records()

    # Get current date
    today = datetime.today().date()  # Convert to date
    one_week_ago = (datetime.today() - timedelta(days=7)).date()  # Convert to date
    first_day_of_month = today.replace(day=1)

    # Create a table to track milk production per cow
    weekly_data = {cow.id: 0 for cow in all_cows}
    monthly_data = {cow.id: 0 for cow in all_cows}

    # Calculate weekly and monthly milk production for each cow
    for record in milk_records:
        # Ensure that record.record_date is compared with date objects
        if record.record_date >= one_week_ago:
            weekly_data[record.cow_id] += record.milk_quantity
        if record.record_date >= first_day_of_month:
            monthly_data[record.cow_id] += record.milk_quantity

    # Clear previous data from the tables
    for widget in weekly_table.get_children():
        weekly_table.delete(widget)
    for widget in monthly_table.get_children():
        monthly_table.delete(widget)

    # Populate weekly and monthly milk production tables
    for cow in all_cows:
        weekly_table.insert('', 'end', values=(cow.name, weekly_data[cow.id]))
        monthly_table.insert('', 'end', values=(cow.name, monthly_data[cow.id]))


root = tk.Tk()
root.title('Dairy Management Dashboard')
root.geometry('1200x800')

# Top Buttons for Navigation
top_buttons_frame = ttk.Frame(root, padding=10)
top_buttons_frame.pack(side=tk.TOP, fill=tk.X)

button_1 = ttk.Button(top_buttons_frame, text='Add Cow Record', command=open_add_cow)
button_2 = ttk.Button(top_buttons_frame, text='Manage Milk Records', command=open_milk_records)
button_3 = ttk.Button(top_buttons_frame, text='Manage Feed Records', command=open_feed_records)
button_quit = ttk.Button(top_buttons_frame, text="Quit Application", command=root.quit)

button_1.pack(side=tk.LEFT, padx=10)
button_2.pack(side=tk.LEFT, padx=10)
button_3.pack(side=tk.LEFT, padx=10)
button_quit.pack(side=tk.LEFT, padx=10)

# Main Dashboard Frame
dashboard_frame = ttk.Frame(root)
dashboard_frame.pack(fill=tk.BOTH, expand=True)

# Left Frame: Cow Information with Delete Buttons
left_frame = ttk.Frame(dashboard_frame, padding=10, borderwidth=2, relief="solid")
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

all_cows_label = ttk.Label(left_frame, text="All Cows", font=("Arial", 14))
all_cows_label.pack(anchor="w")

# Table for cows (Treeview)
columns = ('Name', 'Breed')
all_cows_table = ttk.Treeview(left_frame, columns=columns, show='headings')
all_cows_table.heading('Name', text='Name')
all_cows_table.heading('Breed', text='Breed')

# Add scrollbar to the cows table
cows_scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=all_cows_table.yview)
all_cows_table.configure(yscroll=cows_scrollbar.set)
cows_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
all_cows_table.pack(fill=tk.BOTH, expand=True)

# Middle Frame: Milk Production Graph and Weekly/Monthly Production
middle_frame = ttk.Frame(dashboard_frame, padding=10, borderwidth=2, relief="solid")
middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

graph_label = ttk.Label(middle_frame, text="Milk Production Comparison", font=("Arial", 14))
graph_label.pack(anchor="w")

# Show milk production comparison as a graph
fig = create_milk_graph()
canvas = FigureCanvasTkAgg(fig, master=middle_frame)
canvas.draw()
canvas.get_tk_widget().pack()

# Weekly/Monthly Milk Production Section
milk_production_frame = ttk.Frame(middle_frame, padding=10)
milk_production_frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(milk_production_frame, text="Weekly Milk Production", font=("Arial", 12)).pack(anchor="w")
weekly_columns = ('Cow Name', 'Total Milk')
weekly_table = ttk.Treeview(milk_production_frame, columns=weekly_columns, show='headings')
weekly_table.heading('Cow Name', text='Cow Name')
weekly_table.heading('Total Milk', text='Total Milk (Liters)')
weekly_table.pack(fill=tk.BOTH, expand=True)

ttk.Label(milk_production_frame, text="Monthly Milk Production", font=("Arial", 12)).pack(anchor="w", pady=5)
monthly_columns = ('Cow Name', 'Total Milk')
monthly_table = ttk.Treeview(milk_production_frame, columns=monthly_columns, show='headings')
monthly_table.heading('Cow Name', text='Cow Name')
monthly_table.heading('Total Milk', text='Total Milk (Liters)')
monthly_table.pack(fill=tk.BOTH, expand=True)

# Right Frame: Last 25 Feed Records
right_frame = ttk.Frame(dashboard_frame, padding=10, borderwidth=2, relief="solid")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

feed_records_label = ttk.Label(right_frame, text="Last 25 Feed Records", font=("Arial", 14))
feed_records_label.pack(anchor="w")

# Table for feed records (Treeview)
feed_columns = ('Cow', 'Feed Type', 'Quantity', 'Date')
feed_records_table = ttk.Treeview(right_frame, columns=feed_columns, show='headings')
feed_records_table.heading('Cow', text='Cow')
feed_records_table.heading('Feed Type', text='Feed Type')
feed_records_table.heading('Quantity', text='Quantity')
feed_records_table.heading('Date', text='Date')

# Add scrollbar to the feed records table
feed_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=feed_records_table.yview)
feed_records_table.configure(yscroll=feed_scrollbar.set)
feed_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
feed_records_table.pack(fill=tk.BOTH, expand=True)

# Load the initial cow list and feed records
refresh_cow_list()
show_feed_records()
show_weekly_monthly_production()

root.mainloop()
