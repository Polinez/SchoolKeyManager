import sqlite3

from classes.locker import Locker
from classes.schoolClass import Class
from classes.key import Key



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
                             status BOOLEAN)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS keys
                        (id INTEGER PRIMARY KEY,
                        number INTEGER,
                        schoolClass TEXT,
                        lockerId INTEGER,
                        status TEXT,
                        FOREIGN KEY (lockerId) REFERENCES lockers(id))''')
        conn.commit()
    except sqlite3.Error as e:
        raise Exception("Błąd:",f"Podczas tworzenia bazy: {e}")
    finally:
        if conn:
            conn.close()

def import_from_db_to_lists():
    classList = []
    lockersList = []
    keysList = []
    create_db()
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

        # Import keys
        cursor.execute("SELECT * FROM keys")
        rows = cursor.fetchall()
        for row in rows:
            keysList.append(Key(row[1], row[2], row[4]))

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

def update_class_in_db(school_class: Class):
    try:
        conn = sqlite3.connect('dataBase/DataBase.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE classes SET numberOfStudents = ? WHERE className = ?",
                           (school_class.number_of_students, school_class.name))
        conn.commit()
    except sqlite3.Error as e:
        raise Exception("Błąd", f"Podczas aktualizowania klasy w bazie: {e}")
    finally:
        if conn:
            conn.close()

def delete_class_from_db(school_class: Class):
    try:
        conn = sqlite3.connect('dataBase/DataBase.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM classes WHERE className = ?",
                           (school_class.name,))
        conn.commit()
    except sqlite3.Error as e:
        raise Exception("Błąd", f"Podczas usuwania klasy z bazy: {e}")
    finally:
        if conn:
            conn.close()

def add_locker_to_db(locker: Locker):
    try:
        conn = sqlite3.connect('dataBase/DataBase.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO lockers (number, room, row, column, status) VALUES (?, ?, ?, ?, ?)",
                           (locker.number,locker.room, locker.position[0], locker.position[1], locker.key_assigned))
        conn.commit()
    except sqlite3.Error as e:
        raise Exception("Błąd", f"Podczas dodawawania szafki do bazy: {e}")
    finally:
        if conn:
            conn.close()

def delete_locker_from_db(locker: Locker):
    try:
        conn = sqlite3.connect('dataBase/DataBase.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM lockers WHERE number = ?",
                           (locker.number,))
        conn.commit()
    except sqlite3.Error as e:
        raise Exception("Błąd", f"Podczas usuwania szafki z bazy: {e}")
    finally:
        if conn:
            conn.close()

def update_locker_status_in_db(locker: Locker):
    try:
        conn = sqlite3.connect('dataBase/DataBase.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE lockers SET status = ? WHERE number = ?",
                           (locker.key_assigned, locker.number))
        conn.commit()
    except sqlite3.Error as e:
        raise Exception("Błąd", f"Podczas aktualizowania szafki w bazie: {e}")
    finally:
        if conn:
            conn.close()

def update_locker_position_in_db(locker: Locker):
    try:
        conn = sqlite3.connect('dataBase/DataBase.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE lockers SET room = ?, row = ?, column = ? WHERE number = ?",
                           (locker.room, locker.position[0], locker.position[1], locker.number))
        conn.commit()
    except sqlite3.Error as e:
        raise Exception("Błąd", f"Podczas aktualizowania szafki w bazie: {e}")
    finally:
        if conn:
            conn.close()

def add_key_to_db(key: Key):
    try:
        conn = sqlite3.connect('dataBase/DataBase.db')
        cursor = conn.cursor()

        # Znajdź odpowiednią szafkę na podstawie numeru szafki
        cursor.execute("SELECT id FROM lockers WHERE number = ?",
                       (key.number,))
        locker_id = cursor.fetchone()

        if locker_id is None:
            raise Exception("Szafka o podanym numerze nie istnieje.")

        locker_id = locker_id[0]

        # Dodaj klucz do bazy
        cursor.execute("INSERT INTO keys (number, schoolClass, lockerId, status) VALUES (?, ?, ?, ?)",
                       (key.number,key.keyclass ,locker_id, key.status))
        conn.commit()

    except sqlite3.Error as e:
        raise Exception("Błąd", f"Podczas dodawania klucza do bazy: {e}")
    finally:
        if conn:
            conn.close()

def update_key_status_in_db(key: Key):
    try:
        conn = sqlite3.connect('dataBase/DataBase.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE keys SET schoolClass = ?, status = ? WHERE number = ?",
                            (key.keyclass, key.status, key.number))
        conn.commit()
    except sqlite3.Error as e:
        raise Exception("Błąd", f"Podczas aktualizowania klucza w bazie: {e}")
    finally:
        if conn:
            conn.close()

def delete_key_from_db(key: Key):
    try:
        conn = sqlite3.connect('dataBase/DataBase.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM keys WHERE number = ?",
                           (key.number,))
        conn.commit()
    except sqlite3.Error as e:
        raise Exception("Błąd", f"Podczas usuwania klucza z bazy: {e}")
    finally:
        if conn:
            conn.close()


