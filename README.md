# 🔑 School Key and Locker Management Application
---
## 📚 Project Description
This Python application, developed with the tkinter library, facilitates the management of keys, lockers, and school classes. The system aids in organizing space by allowing the assignment of keys to specific lockers and managing their availability.

### ✨ Features
<details>
<summary>Click to see the Features</summary>
  
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

</details>

### ⚙️ Technologies Used
<details>
<summary>Click to see the Technologies</summary>
  
Python: Main programming language.

Tkinter: GUI library for creating the user interface.

SQLite: Local database for storing information about keys, lockers, and classes.

FPDF: Generating reports in PDF format (future feature).

Modularity: Code divided into modules (actions, classes, database, styles) for easy management and development.

</details>

### 🗂️ Project Structure
```
SchoolKeyMenager/
│
├── main.py    # main folder 
|
├── actions/                # all actions like save/add/refresh
│   ├── class_actions.py    
│   ├── keys_actions.py     
│   ├── lockers_actions.py 
│   └── main_actions.py     
│
├── classes/                # all class objects of keys/lockers/schoolClasses
│   ├── key.py          
│   ├── locker.py        
│   └── schoolClass.py      
│
├── dataBase/
│   ├── data.py                 # Database operations
|   └── DataBase.db             # SQLite database
│
├── keyicon.ico             # app icon
├── lists.py                # lists of objects of keys/lockers/classes              
├── styles.py                   # GUI style definitions
│
├── requirements.txt            # Dependency list
└── README.md                   # Project documentation
```

<img width="816" alt="Main Menu" src="https://github.com/user-attachments/assets/b97ac4bd-39b8-422c-bf6a-889474a6c148" />


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
This software is proprietary and not open-source. Unauthorized use is prohibited. For licensing inquiries, please contact sebastianwandzel@yahoo.pl.

