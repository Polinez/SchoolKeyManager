import os
import re
from tkinter import messagebox
# pdf
from fpdf import FPDF
from unidecode import unidecode
#database
from dataBase.data import *
# lists
from lists import keysList, lockersList

# Display keys in the table
def refresh_key_table(key_table):
        for item in key_table.get_children():
            key_table.delete(item)  # Remove existing entries
        for k in keysList:
            key_table.insert("", "end", values=(k.ID, k.number, k.keyclass, k.status))

def add_to_key_table(key, key_table):
        key_table.insert("", "end", values=(key.ID, key.number, key.keyclass, key.status))


def add_key_action(key_nr, key_class, key_table):
    try:
        if key_nr.get() == "":
            messagebox.showwarning("Brak danych", "Nie podano numeru klucza.")
            return

        if not re.match("^[0-9]{4}$", key_nr.get()):
            messagebox.showerror("Błąd", "Numer klucza musi się składać z 4 cyfr np. 1234")
            return

        # if key number matches the number of any locker
        if not any(l.number == int(key_nr.get()) for l in lockersList):
            messagebox.showerror("Błąd", "Nie ma szafki do której pasowałby ten klucz.")
            return

        # handle if key is in class or if user want to change class of an assigned key
        for k in keysList:
            if k.number == int(key_nr.get()):
                if k.keyclass == key_class.get():
                    messagebox.showerror("Błąd",
                                         f"Klucz o podanym numerze jest juz przypisany do klasy {key_class.get()}.")
                    return
                else:
                    update = messagebox.askyesno(
                        "Aktualizacja klucza",
                        f"Klucz o numerze {key_nr.get()} już istnieje i jest przypisany do {k.keyclass}, chcesz przypisać go do {key_class.get()}?"
                    )
                    if update:
                        k.keyclass = key_class.get()
                        if key_class.get() == "Koszyk":
                            k.status = "Dostępny"
                        else:
                            k.status = "Wypożyczony"
                        # update db
                        update_key_status_in_db(k)
                        # refresh Treeview
                        refresh_key_table(key_table)
                        messagebox.showinfo("Sukces",
                                            f"Klucz {key_nr.get()} został przypisany pomyślnie do nowego miejsca.")
                        return
                    else:
                        return

        number = int(key_nr.get())
        keyclass = key_class.get()

        if keyclass == "Koszyk":
            status = "Dostępny"
        else:
            status = "Wypożyczony"

        key = Key(number, keyclass, status)
        # adding to list
        keysList.append(key)
        # adding to Treeview
        add_to_key_table(key, key_table)
        # adding to db
        add_key_to_db(key)
        # change locker status
        for l in lockersList:
            if l.number == number:
                l.key_assigned = True
                update_locker_status_in_db(l)
        messagebox.showinfo("Sukces", f"Klucz {key_nr.get()} dodany pomyślnie do {key_class.get()}.")
    except ValueError:
        messagebox.showerror("Błąd", "Numer klucza musi być liczbą całkowitą.")
        return
    except Exception as e:
        messagebox.showerror("Błąd", f"{e}")
        return


def find_key_action(key_nr):
    if key_nr.get() == "":
        messagebox.showwarning("Brak danych", "Nie podano numeru klucza do wyszukania.")
        return

    if len(key_nr.get()) != 4:
        messagebox.showerror("Błąd", "Numer klucza musi się składać z 4 cyfr np. 1234")
        return

    for key in keysList:
        if int(key_nr.get()) == key.number:
            messagebox.showinfo("Pozycja klucza", f"Klucz który szukasz jest przypisany do: {key.keyclass}.")
            return
    else:
        messagebox.showwarning("Brak klucza", "Nie ma klucza o takim numerze.")
        return


# saves keys to pdf
def save_keys_action(class_name):
    if class_name.get() == "Wszystkie":
        keys = keysList
    else:
        keys = [k for k in keysList if k.keyclass == class_name.get()]

    if not keys:
        messagebox.showinfo("Info", "Brak kluczy do zapisu.")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    pdf.cell(200, 10, "Lista Kluczy", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)  # line break

    # sorting by key number
    keys = sorted(keys, key=lambda x: x.number)

    for key in keys:
        key_text = f"Klucz: {key.number}, Przypisany do klasy: {key.keyclass}"
        pdf.cell(0, 4, unidecode(key_text), new_x="LMARGIN", new_y="NEXT")

    try:
        output_dir = "PDF"
        pdf_file = os.path.join(output_dir, "klucze.pdf")
        os.makedirs(output_dir, exist_ok=True)
        pdf.output(pdf_file)
        messagebox.showinfo("Info",
            f"Klucze zostały zapisane do pliku {pdf_file} w folderze aplikacji. \nMożesz teraz je wydrukować.")
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas zapisu pliku PDF: {e}")