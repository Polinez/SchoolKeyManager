import re
from tkinter import messagebox

from dataBase.data import *

# lists
from lists import classList


# Displaying all school classes
def refresh_class_table(class_table):
    for item in class_table.get_children():
        class_table.delete(item)  # Remove existing entries

    for c in classList:
        class_table.insert("", "end", values=(c.ID, c.name, c.number_of_students))

# on button click add class to list
def add_class_action(class_name, class_number,class_table):
    try:
        if class_name.get() == "" or class_number.get() == "":
            messagebox.showwarning("Brak danych", "Nie podano wszystkich danych.")
            return

        if not re.match("^[0-9][A-Z]$", class_name.get()):
            messagebox.showerror("Błąd", "Nazwa musi się składać z cyfry i dużej litery. np 1A, 2B.")
            return
        # check if user don't want to change number of students in class
        for c in classList:
            if c.name == class_name.get():
                if c.number_of_students == int(class_number.get()):
                    messagebox.showerror("Błąd", "Klasa o podanej nazwie i liczbie uczniów już istnieje.")
                    return
                else:
                    update = messagebox.askyesno(
                        "Aktualizacja klasy",
                        f"Klasa {c.name} już istnieje, chcesz zaktualizować jej liczbę uczniów na {class_number.get()}?"
                    )
                    if update:
                        c.number_of_students = int(class_number.get())
                        update_class_in_db(c)
                        refresh_class_table(class_table)
                        messagebox.showinfo("Sukces", f"Klasa {class_name.get()} zaktualizowana pomyślnie.")
                        return
                    else:
                        return

        if int(class_number.get()) < 0:
            messagebox.showerror("Błąd", "Liczba uczniów w klasie nie może być ujemna.")
            return

        name = class_name.get()
        number = int(class_number.get())
        school_class = Class(name, number)
        # adding to list
        classList.append(school_class)
        # adding to db
        add_class_to_db(school_class)
        # refresh the table
        refresh_class_table(class_table)
        messagebox.showinfo("Sukces", f"Klasa {class_name.get()} dodana pomyślnie.")
    except ValueError:
        messagebox.showerror("Błąd", "Liczba uczniów w klasie musi być liczbą całkowitą.")
        return
    except Exception as e:
        messagebox.showerror("Błąd", f"{e}")
        return