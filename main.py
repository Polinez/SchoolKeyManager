# tkinter
import re
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox

# Database
from dataBase.data import *

# objects
from classes.key import Key
from classes.schoolClass import Class
from classes.locker import Locker
# styles
from styles import *
# PDFs
from fpdf import FPDF
from save_to_PDF import save_to_pdf


def clear_frame():
    for widget in content_frame.winfo_children():
        widget.destroy()


def button_back():
    return Button(content_frame,text="Wróć",**BUTTON_STYLE,command=main)

# Funkcje dla poszczególnych opcji menu

def add_key():
    mainPage.update()
    clear_frame()
    back_btn = button_back()
    back_btn.place(x=10, y=10)
    title = Label(content_frame, text="Dodaj/Edytuj klucz", **MAIN_LABEL_STYLE)
    title.pack(pady=20)

    def find_key_action():
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
            messagebox.showwarning("Brak klucza", "Nie ma szafki o takim numerze.")
            return


    find_locker_btn = Button(content_frame, text="Znajdz klucz", **BUTTON_STYLE, command=find_key_action)
    find_locker_btn.place(x=660, y=10)

    key_nr_lb = Label(content_frame, text="Numer klucza", **LABEL_STYLE)
    key_nr_lb.pack(pady=10)
    key_nr = Entry(content_frame, **ENTRY_STYLE)
    key_nr.pack()

    key_class_lb = Label(content_frame, text="Przypisz do klasy", **LABEL_STYLE)
    key_class_lb.pack(pady=10)
    key_class = Combobox(content_frame, values=["Koszyk"]+[c.name for c in classList], state="readonly", **COMBOBOX_STYLE)
    key_class.pack()
    key_class.current(0)


    def add_key_action():
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
                        messagebox.showerror("Błąd", f"Klucz o podanym numerze jest juz przypisany do klasy {key_class.get()}.")
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
                            refresh_key_table()
                            messagebox.showinfo("Sukces", f"Klucz {key_nr.get()} został przypisany pomyślnie do nowego miejsca.")
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
            add_to_key_table(key)
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


    key_button = Button(content_frame, text="Dodaj klucz", **BUTTON_STYLE, command=add_key_action)
    key_button.pack(pady=20)

    key_list_label = Label(content_frame, text="Lista kluczy", **MAIN_LABEL_STYLE)
    key_list_label.pack(pady=20)

    # Treeview for keys
    key_table = Treeview(content_frame, columns=("ID", "Numer", "Przypisany do klasy", "Status"), show="headings", )
    key_table.pack(fill=BOTH, expand=True, padx=20)

    # Define columns and their headings
    key_table.heading("ID", text="ID")
    key_table.heading("Numer", text="Numer klucza")
    key_table.heading("Przypisany do klasy", text="Przypisany do klasy/koszyka")
    key_table.heading("Status", text="Status")

    # Adjust column width
    key_table.column("ID", width=50)
    key_table.column("Numer", width=100)
    key_table.column("Przypisany do klasy", width=150)
    key_table.column("Status", width=100)

    # Display keys in the table
    def refresh_key_table():
        for item in key_table.get_children():
            key_table.delete(item)  # Remove existing entries
        for k in keysList:
            key_table.insert("", "end", values=(k.ID, k.number, k.keyclass, k.status))

    def add_to_key_table(key):
        key_table.insert("", "end", values=(key.ID, key.number, key.keyclass, key.status))

    mainPage.update()
    refresh_key_table()




def add_locker():
    mainPage.update()
    clear_frame()
    back_btn = button_back()
    back_btn.place(x=10, y=10)
    title = Label(content_frame, text="Dodaj/Edytuj szafkę", **MAIN_LABEL_STYLE)
    title.pack(pady=20)

    def find_locker_action():
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


    find_locker_btn = Button(content_frame, text="Znajdz szafke", **BUTTON_STYLE, command=find_locker_action)
    find_locker_btn.place(x=650, y=10)

    locker_nr_label = Label(content_frame, text="Numer szafki", **LABEL_STYLE)
    locker_nr_label.pack(pady=10)
    locker_nr = Entry(content_frame, **ENTRY_STYLE)
    locker_nr.pack()

    # Frame for details
    locker_details_frame = Frame(content_frame, **FRAME_STYLE)
    locker_details_frame.pack(pady=10)

    # Room
    locker_room_label = Label(locker_details_frame, text="Sala", **LABEL_STYLE)
    locker_room_label.grid(row=0, column=0, padx=5, pady=10, sticky="n", columnspan=2)
    locker_room = Combobox(locker_details_frame, values=["Szkola Podstawowa", "Liceum"], state="readonly",**COMBOBOX_STYLE)
    locker_room.grid(row=1, column=0, padx=5, columnspan=2)
    locker_room.current(0)

    # ROW
    locker_row_label = Label(locker_details_frame, text="Rząd", **LABEL_STYLE)
    locker_row_label.grid(row=0, column=2, padx=5, pady=10, sticky="n", columnspan=2)
    locker_row = Combobox(locker_details_frame, values=["Gora", "Dol"], state="readonly", **COMBOBOX_STYLE)
    locker_row.grid(row=1, column=2, padx=5,  columnspan=2)
    locker_row.current(0)

    # Column
    locker_column_label = Label(locker_details_frame, text="Kolumna", **LABEL_STYLE)
    locker_column_label.grid(row=0, column=4, padx=5, pady=10, sticky="n", columnspan=2)
    locker_column = Entry(locker_details_frame, **ENTRY_STYLE)
    locker_column.grid(row=1, column=4, padx=5, columnspan=2)

    def add_locker_action():
        try:
            if locker_nr.get() == ""   or locker_column.get() == "":
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
                            refresh_locker_table()
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
            refresh_locker_table()
            # adding to db
            add_locker_to_db(locker)
            messagebox.showinfo("Sukces", f"Szafka {number} dodana pomyślnie.")
        except ValueError:
            messagebox.showerror("Błąd", "Numer szafki, rząd i kolumna muszą być liczbami całkowitymi.")
            return
        except Exception as e:
            messagebox.showerror("Błąd", f"{e}")
            return

    locker_button = Button(content_frame, text="Dodaj szafkę", **BUTTON_STYLE,command=add_locker_action)
    locker_button.pack(pady=20)

    locker_list_label = Label(content_frame, text="Lista szafek", **MAIN_LABEL_STYLE)
    locker_list_label.pack()


    save_lockers_btn = Button(content_frame, text="Zapisz szafki do PDF", **BUTTON_STYLE,command=save_to_pdf.save_lockers_action)
    save_lockers_btn.pack(pady=10)

    # Treeview for lockers
    locker_table = Treeview(content_frame, columns=("ID", "Numer", "Pokój", "Pozycja", "Klucz Przydzielony"), show="headings",)
    locker_table.pack(fill=BOTH, expand=True, padx=20)

    # Define columns and their headings
    locker_table.heading("ID", text="ID")
    locker_table.heading("Numer", text="Numer")
    locker_table.heading("Pokój", text="Pokój")
    locker_table.heading("Pozycja", text="Pozycja")
    locker_table.heading("Klucz Przydzielony", text="Czy klucz przydzielony do szafki?")

    # Adjust column width
    locker_table.column("ID", width=50)
    locker_table.column("Numer", width=100)
    locker_table.column("Pokój", width=150)
    locker_table.column("Pozycja", width=100)
    locker_table.column("Klucz Przydzielony", width=150)

    # Display lockers in the table
    def refresh_locker_table():
        for item in locker_table.get_children():
            locker_table.delete(item)  # Remove existing entries
        for l in lockersList:
            locker_table.insert("", "end", values=(l.ID, l.number, l.room, str(l.position), "Przydzielony" if l.key_assigned else "Nie przydzielony"))

    mainPage.update()
    refresh_locker_table()


# Dodaj klase

def add_class():
    mainPage.update()
    clear_frame()
    back_btn = button_back()
    back_btn.place(x=10, y=10)
    title = Label(content_frame, text="Dodaj/Edytuj klasę", **MAIN_LABEL_STYLE)
    title.pack(pady=20)

    class_name_label = Label(content_frame, text="Nazwa klasy", **LABEL_STYLE)
    class_name_label.pack(pady=10)
    class_name = Entry(content_frame, **ENTRY_STYLE)
    class_name.pack()

    class_number_label = Label(content_frame, text="Liczba uczniów w klasie", **LABEL_STYLE)
    class_number_label.pack(pady=10)
    class_number = Entry(content_frame, **ENTRY_STYLE)
    class_number.pack()

    # on button click add class to list
    def add_class_action():
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
                            refresh_class_table()
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
            refresh_class_table()
            messagebox.showinfo("Sukces", f"Klasa {class_name.get()} dodana pomyślnie.")
        except ValueError:
            messagebox.showerror("Błąd", "Liczba uczniów w klasie musi być liczbą całkowitą.")
            return
        except Exception as e:
            messagebox.showerror("Błąd", f"{e}")
            return

    class_button = Button(content_frame, text="Dodaj klasę", **BUTTON_STYLE, command=add_class_action)
    class_button.pack(pady=20)

    # Treeview for displaying classes
    class_table = Treeview(content_frame, columns=("ID", "Nazwa klasy", "Liczba uczniów"), show="headings",)
    class_table.pack(fill=BOTH, expand=True, padx=20, pady=20)

    # Define columns and their headings
    class_table.heading("ID", text="ID")
    class_table.heading("Nazwa klasy", text="Nazwa klasy")
    class_table.heading("Liczba uczniów", text="Liczba uczniów")

    # Adjust column width
    class_table.column("ID", width=50)
    class_table.column("Nazwa klasy", width=150)
    class_table.column("Liczba uczniów", width=150)

    # Displaying all school classes
    def refresh_class_table():
        for item in class_table.get_children():
            class_table.delete(item)  # Remove existing entries

        for c in classList:
            class_table.insert("", "end", values=(c.ID, c.name, c.number_of_students))

    refresh_class_table()

    mainPage.update()


def save_keys():
    mainPage.update()
    clear_frame()
    back_btn = button_back()
    back_btn.place(x=10, y=10)
    title = Label(content_frame, text="Zapisz klucze do pliku PDF", **MAIN_LABEL_STYLE)
    title.pack(pady=20)

    label = Label(content_frame, text="Wybierz klasę", **LABEL_STYLE)
    label.pack(pady=10)

    class_name = Combobox(content_frame, values=["Wszystkie"]+[c.name for c in classList], state="readonly", **COMBOBOX_STYLE)
    class_name.pack()
    class_name.bind("<<ComboboxSelected>>", lambda event: refresh_key_table())


    save_key = Button(content_frame, text="Zapisz", **BUTTON_STYLE, command=lambda: save_to_pdf.save_keys_action(class_name))
    save_key.pack(pady=20)


    # tree view for displaying keys
    key_table = Treeview(content_frame, columns=("Numer", "Przypisany do klasy"), show="headings",)
    key_table.pack(fill=BOTH, expand=True, padx=250, pady=20)

    # # Define columns and their headings
    key_table.heading("Numer", text="Numer klucza")
    key_table.heading("Przypisany do klasy", text="Przypisany do klasy/koszyka")

    # Adjust column width
    key_table.column("Numer", width=100)
    key_table.column("Przypisany do klasy", width=100)

    # Display keys in the table
    def refresh_key_table():
        for item in key_table.get_children():
            key_table.delete(item)
        for k in keysList:
            if class_name.get() == "Wszystkie" or k.keyclass == class_name.get():
                key_table.insert("", "end", values=(k.number, k.keyclass))

    refresh_key_table()
    mainPage.update()





# Main window
def main():
    mainPage.update()
    clear_frame()

    title = Label(content_frame, text="Menedżer kluczy", **MAIN_LABEL_STYLE)
    title.pack(pady=20)

    # Frame for buttons
    button_frame = Frame(content_frame, **FRAME_STYLE)
    button_frame.pack(fill=X, pady=20)

    buttons = [
        ("Klucze", add_key),
        ("Szafki", add_locker),
        ("Klasy", add_class),
        ("Zapisz klucze", save_keys)
    ]

    for text, command in buttons:
        button = Button(button_frame, text=text, **BUTTON_STYLE, command=command)
        button.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

    error_label = Label(content_frame, text="Błędy", **MAIN_LABEL_STYLE)
    error_label.pack(pady=20)

    # Treeview for errors
    error_table = Treeview(content_frame, columns=("Typ", "Wiadomość"), show="headings", )
    error_table.pack(fill=BOTH, expand=True, padx=20)

    # Define columns and their headings
    error_table.heading("Typ", text="Typ")
    error_table.heading("Wiadomość", text="Wiadomość")

    # Adjust column width
    error_table.column("Typ", width=80)
    error_table.column("Wiadomość", width=800)

    # Displaying all lockers with no keys assigned and keys with no class assigned
    def refresh_error_table():
        for item in error_table.get_children():
            error_table.delete(item)  # Remove existing entries

        for l in lockersList:
            if not l.key_assigned:
                error_table.insert("", "end", values=("Szafka", str(l.display_if_key_not_assigned())))

        for k in keysList:
            if k.keyclass == "Koszyk":
                error_table.insert("", "end", values=("Klucz", str(k.display_if_not_assigned())))

    refresh_error_table()

    mainPage.update()



# Główna pętla aplikacji
if __name__ == "__main__":
    # Main window config
    mainPage = Tk()
    mainPage.title("Menedżer kluczy")
    mainPage.geometry("820x640")
    mainPage.configure(bg="white")
    mainPage.resizable(False, False)

    # main frame to hold all content
    content_frame = Frame(mainPage, **FRAME_STYLE)
    content_frame.pack(fill=BOTH, expand=True)

    # Create database
    create_db()
    # importing list of objects form database
    classList, keysList, lockersList = import_from_db_to_lists()
    # Run
    main()
    mainPage.mainloop()

