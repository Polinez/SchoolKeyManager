import sqlite3

from classes.locker import Locker
from classes.schoolClass import Class



def create_db():
    try:
        conn = sqlite3.connect('dataBase/DataBase.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS classes
                        (id INTEGER PRIMARY KEY,
                         className TEXT,
                          numberOfStudents INTEGER)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS lockers 
                        (id INTEGER PRIMARY KEY,
                         number INTEGER,
                          room TEXT,
                           row INTEGER,
                            column INTEGER,
                             status TEXT)''')
        conn.commit()
    except sqlite3.Error as e:
        raise Exception("Błąd:",f"Podczas tworzenia bazy: {e}")
    finally:
        if conn:
            conn.close()

def import_from_db_to_lists(classList: list, keysList: list, lockersList: list):

    try:
        conn = sqlite3.connect('dataBase/DataBase.db')
        cursor = conn.cursor()

        # Import classes
        cursor.execute("SELECT * FROM classes")
        rows = cursor.fetchall()
        for row in rows:
            classList.append(Class(row[1], row[2]))

        # Import lockers
        cursor.execute("SELECT * FROM lockers")
        rows = cursor.fetchall()
        for row in rows:
            lockersList.append(Locker(row[1], row[2], row[3], row[4], row[5]))

    except sqlite3.Error as e:
        raise Exception("Błąd:",f"Podczas importowania bazy: {e}")
    finally:
        if conn:
            conn.close()
    return classList, keysList, lockersList

def add_class_to_db(schoolClass: Class):
    try:
        conn = sqlite3.connect('dataBase/DataBase.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO classes (className, numberOfStudents) VALUES (?, ?)",
                           (schoolClass.name, schoolClass.number_of_students))
        conn.commit()
    except sqlite3.Error as e:
        raise Exception("Błąd", f"Podczas dodawania klasy do bazy:{e}")
    finally:
        if conn:
            conn.close()

def add_locker_to_db(locker):
    try:
        conn = sqlite3.connect('dataBase/DataBase.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO lockers (number, room, row, column, status) VALUES (?, ?, ?, ?, ?)",
                           (locker.number,locker.room, locker.position[0], locker.position[1], locker.status))
        conn.commit()
    except sqlite3.Error as e:
        raise Exception("Błąd", f"Podczas dodawawania szafki do bazy: {e}")
    finally:
        if conn:
            conn.close()
