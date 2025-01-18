import re
from tkinter import messagebox
from fpdf import FPDF
from unidecode import unidecode

from dataBase.data import *

# lists
from lists import lockersList


# Display lockers in the table
def refresh_locker_table(locker_table):
        for item in locker_table.get_children():
            locker_table.delete(item)  # Remove existing entries
        for l in lockersList:
            locker_table.insert("", "end", values=(l.ID, l.number, l.room, str(l.position), "Przydzielony" if l.key_assigned else "Nie przydzielony"))


def add_locker_action(locker_nr, locker_room, locker_row, locker_column,locker_table):
    try:
        if locker_nr.get() == "" or locker_column.get() == "":
            messagebox.showwarning("Brak danych", "Nie podano wszystkich danych.")
            return

        if not locker_nr.get().isdigit() or not locker_column.get().isdigit():
            messagebox.showerror("Błąd", "Numer szafki oraz kolumna muszą być liczbami całkowitymi.")
            return

        if not re.match("^[0-9]{4}$", locker_nr.get()):
            messagebox.showerror("Błąd", "Numer szafki musi się składać z 4 cyfry np. 1234")
            return

        # assighning values
        row = locker_row.get()
        number = int(locker_nr.get())
        room = locker_room.get()
        column = int(locker_column.get())

        for l in lockersList:
            if l.number == number:
                if l.room == room and l.position == (row, column):
                    messagebox.showerror("Błąd", "Probujesz dodać szafkę która juz istnieje. (DUPLIKAT)")
                    return
                else:
                    update = messagebox.askyesno(
                        "Aktualizacja szafki",
                        f"Szafka o numerze {number} już istnieje, chcesz zaktualizować jej położenie na {room}, {row}, {column}?"
                    )
                    if update:
                        l.room = room
                        l.position = (row, column)
                        # update db posiotion
                        update_locker_position_in_db(l)
                        # refresh table
                        refresh_locker_table(locker_table)
                        messagebox.showinfo("Sukces", f"Szafka {number} zaktualizowana pomyślnie.")
                        return
                    else:
                        return
            if l.room == room and l.position == (row, column):
                messagebox.showerror("Błąd", f"Szafka nr {l.number} stoi na tym polozeniu.")
                return

        locker = Locker(number, room, row, column, False)
        # adding to list
        lockersList.append(locker)
        # adding to table
        refresh_locker_table(locker_table)
        # adding to db
        add_locker_to_db(locker)
        messagebox.showinfo("Sukces", f"Szafka {number} dodana pomyślnie.")
    except ValueError:
        messagebox.showerror("Błąd", "Numer szafki, rząd i kolumna muszą być liczbami całkowitymi.")
        return
    except Exception as e:
        messagebox.showerror("Błąd", f"{e}")
        return

def find_locker_action(locker_nr):
    if locker_nr.get() == "":
        messagebox.showwarning("Brak danych", "Nie podano numeru szafki do wyszukania.")
        return

    if len(locker_nr.get()) != 4:
        messagebox.showerror("Błąd", "Numer szafki musi się składać z 4 cyfr np. 1234")
        return

    for locker in lockersList:
        if int(locker_nr.get()) == locker.number:
            messagebox.showinfo("Pozycja szafki", f"Szafka której szukasz jest w : {locker.room}\npozycja: {locker.position[0]}, kolumna: {locker.position[1]}")
            return
    else:
        messagebox.showwarning("Brak szafki", "Nie ma szafki o takim numerze.")
        return


# saves lockers to pdf
def save_lockers_action():
    if not lockersList:
        messagebox.showinfo("Info", "Brak szafek do zapisu.")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    pdf.cell(200, 10, unidecode("Lista Szafek"), new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)  # line break

    # sorting by locker number
    lockers = sorted(lockersList, key=lambda x: x.number)

    for locker in lockers:
        locker_text = f"Szafka: {locker.number}, {locker.room} {locker.position[0]} {locker.position[1]}"
        pdf.cell(0, 4, unidecode(locker_text), new_x="LMARGIN", new_y="NEXT")

    try:
        pdf_file = "szafki.pdf"
        pdf.output(pdf_file)
        messagebox.showinfo("Info",
            f"Szafki zostały zapisane do pliku {pdf_file} w folderze aplikacji. \nMożesz teraz je wydrukować.")
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas zapisu pliku PDF: {e}")


def change_locker_nr_action(old_locker_nr, new_locker_nr, locker_room, locker_row, locker_column):
    if old_locker_nr.get() == "" or new_locker_nr.get() == "":
        messagebox.showwarning("Brak danych", "Nie podano numeru szafki do zmiany.")
        return

    if not re.match("^[0-9]{4}$", old_locker_nr.get()) or not re.match("^[0-9]{4}$", new_locker_nr.get()):
        messagebox.showerror("Błąd", "Numer szafki musi się składać z 4 cyfr np. 1234")
        return

    for l in lockersList:
        if l.number == int(old_locker_nr.get()):
            if locker_room.get() != l.room or locker_row.get() != l.position[0] or int(locker_column.get()) != int(l.position[1]):
                messagebox.showerror("Błąd", f"Pozycja która podałeś nie zgadza sie z pozycja szafki nr {old_locker_nr.get()}.")
                return

            if l.number == int(new_locker_nr.get()):
                messagebox.showerror("Błąd", "Nowy numer szafki jest taki sam jak stary.")
                return
            else:
                for l2 in lockersList:
                    if l2.number == int(new_locker_nr.get()):
                        messagebox.showerror("Błąd", "Szafka o takim numerze już istnieje.")
                        return
                l.number = int(new_locker_nr.get())
                # update db
                update_locker_in_db(old_locker_nr.get(),l)
                messagebox.showinfo("Sukces", f"Numer szafki {old_locker_nr.get()} został zmieniony na {new_locker_nr.get()}.")
                return
    else:
        messagebox.showerror("Błąd", f"Nie ma szafki o numerze {old_locker_nr.get()}.")