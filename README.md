# Dairy Management System

The **Dairy Management System** is a Python-based application built using `Tkinter` and `SQLAlchemy` to help dairy farmers manage cow records, milk production, and feed information efficiently. It provides a graphical user interface (GUI) to add, update, delete cow records, view milk production data, and manage feed records, all while offering visual insights through graphs and tables.

## running
```
python3 app/model/main_window.py
```
## Features

- **Cow Management**: Add, update, and delete cow records (name, breed, birthdate, and tag number).
- **Milk Production**: Track milk production per cow on a weekly and monthly basis, with visual bar charts comparing production among cows.
- **Feed Management**: Record feed information, view the last 25 feed records, and manage feed records by adding new entries or deleting old ones.
- **Dashboard**: Visual dashboard showing:
  - Milk production comparison across all cows
  - Weekly and monthly milk production per cow in a tabular format
  - Recent feed records
- **Quit Application**: Easily exit the application via a "Quit Application" button.


## Technologies Used

- **Python 3.x**
- **Tkinter**: For creating the GUI components.
- **SQLAlchemy**: For object-relational mapping (ORM) and database interactions.
- **Matplotlib**: For generating graphs and visualizations.
- **SQLite**: Default database used with SQLAlchemy for storing cow, milk, and feed records.

## Installation

### Prerequisites

- **Python 3.x**: Make sure Python is installed on your system.
- **Pip**: Ensure pip is installed for managing Python packages.



