# 🔑 School Key and Locker Management Application
---
## 📚 Project Description
This Python application, developed with the tkinter library, facilitates the management of keys, lockers, and school classes. The system aids in organizing space by allowing the assignment of keys to specific lockers and managing their availability.

### Features
Adding and Editing Keys:
- Assign keys to lockers or classes.
- Validate key numbers (4 digits, e.g., 1234).
- Manage key status (available/borrowed).

Adding and Editing Lockers:
- Define locker numbers (4 digits).
- Specify locker locations (room, row, column).
- Ensure locker uniqueness and manage associated keys.

Adding and Editing Classes:
- Create classes with names (e.g., 1A, 2B) and student counts.
- Update student counts in existing classes.
- Display class lists.

Data Review and Management:
- Display data in tables (Treeview).
- Dynamically refresh tables after changes.
- Integration with an SQLite database.

### ⚙️ Technologies Used
Python: Main programming language.

Tkinter: GUI library for creating the user interface.

SQLite: Local database for storing information about keys, lockers, and classes.

FPDF: Generating reports in PDF format (future feature).

Modularity: Code divided into modules (actions, classes, database, styles) for easy management and development.

### 🗂️ Struktura projektu
```
keyManager/
│
├── main.py                     # Main application file
|
├── dataBase/
│   ├── data.py                 # Database operations
|   └── DataBase.db             # SQLite database
│
├── classes/
│   ├── key.py                  # Class representing a key
│   ├── locker.py               # Class representing a locker
│   ├── schoolClass.py          # Class representing a school class
│
├── styles.py                   # GUI style definitions
│
├── requirements.txt            # Dependency list
└── README.md                   # Project documentation
```

<img width="800" alt="Main Menu" src="https://github.com/user-attachments/assets/43960274-70d0-4895-9363-448edbc9f221" />


## 🚀 How to Run the Application
Download the .zip file from the [Download](https://github.com/Polinez/SchoolKeyMenager/releases) .
The link provides two versions: 
- v0.0.2: For Windows devices with Intel/AMD processors.
- v0.0.1: For Windows devices with ARM processors.

## 🔮 Future Enhancements
- Improved data visualization.
- User management with different access levels (e.g., administrator, teacher).
- Cloud integration for better data synchronization.

# 👨‍💻 Author
The application was created by Sebastian Wandzel as a tool to support the organization managing school keys and as a final project for Python Programming coursework.

## License
The project is released under the MIT license. Details can be found in the LICENSE file.
