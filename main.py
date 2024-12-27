# tkinter
import re
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
# Database
from dataBase.data import *
# objects
from classes.key import Key
from classes.schoolClass import Class
from classes.locker import Locker
# styles
from styles import *


# Main window config
mainPage = Tk()
mainPage.title("Menadżer kluczy")
mainPage.geometry("820x640")
mainPage.configure(bg="white")
mainPage.resizable(False, False)

# main frame to hold all content
content_frame = Frame(mainPage, **FRAME_STYLE)
content_frame.pack(fill=BOTH, expand=True)

# Lists of objects
keysList = []
classList = []
lockersList = []



def clear_frame():
    for widget in content_frame.winfo_children():
        widget.destroy()


def button_back():
    return Button(content_frame,text="Wróć",**BUTTON_STYLE,command=main)

# Funkcje dla poszczególnych opcji menu

# Dodaj klucz
def add_key():
    mainPage.update()
    clear_frame()
    back_btn = button_back()
    back_btn.place(x=10, y=10)
    title = Label(content_frame, text="Dodaj klucz", **MAIN_LABEL_STYLE)
    title.pack(pady=20)

    key_nr_lb = Label(content_frame, text="Numer klucza", **LABEL_STYLE)
    key_nr_lb.pack(pady=10)
    key_nr = Entry(content_frame, **ENTRY_STYLE)
    key_nr.pack()

    key_class_lb = Label(content_frame, text="Przypisz do klasy", **LABEL_STYLE)
    key_class_lb.pack(pady=10)
    key_class = Combobox(content_frame, values=["Brak"]+[c.name for c in classList], state="readonly", **COMBOBOX_STYLE)
    key_class.pack()
    key_class.current(0)


    def add_key_action():
        try:
            if key_nr.get() == "":
                messagebox.showwarning("Brak danych", "Nie podano wszystkich danych.")
                return
            if not any(l.number == int(key_nr.get()) for l in lockersList):
                messagebox.showerror("Błąd", "Nie ma szafki do której pasowałby ten klucz.")
                return
            for k in keysList:
                if k.number == int(key_nr.get()):
                    if k.keyclass == key_class.get():
                        messagebox.showerror("Błąd", "Klucz o podanym numerze i klasie już istnieje.")
                        return
                    else:
                        k.keyclass = key_class.get()
                        k.change_status()
                        # update db
                        update_key_status_in_db(k)
                        # refresh listbox
                        key_listbox.delete(0, END)
                        for k in keysList:
                            key_listbox.insert(END, str(k))
                        # update locker status
                        for l in lockersList:
                            if l.number == k.number:
                                l.key_assigned = True
                                update_locker_status_in_db(l)
                        return

            number = int(key_nr.get())
            keyclass = key_class.get()

            if keyclass == "Brak":
                status = "Dostępny"
            else:
                status = "Wypożyczony"

            key = Key(number, keyclass, status)
            # adding to list
            keysList.append(key)
            # adding to listbox
            key_listbox.insert(END, str(key))
            # adding to db
            add_key_to_db(key)
            # change locker status
            for l in lockersList:
                if l.number == number:
                    l.key_assigned = True
                    update_locker_status_in_db(l)
        except ValueError:
            messagebox.showerror("Błąd", "Numer klucza musi być liczbą całkowitą.")
            return
        except Exception as e:
            messagebox.showerror("Błąd", f"{e}")
            return


    # Przyciski
    key_button = Button(content_frame, text="Dodaj klucz", **BUTTON_STYLE, command=add_key_action)
    key_button.pack(pady=20)

    key_list_label = Label(content_frame, text="Lista kluczy", **MAIN_LABEL_STYLE)
    key_list_label.pack(pady=20)

    key_listbox = Listbox(content_frame, **LISTBOX_STYLE)
    key_listbox.pack(fill=BOTH, expand=True, padx=20)
    mainPage.update()

    # displaying all  keys on listbox
    for k in keysList:
        key_listbox.insert(END, str(k))




# Dodaj szafkę
def add_locker():
    mainPage.update()
    clear_frame()
    back_btn = button_back()
    back_btn.place(x=10, y=10)
    title = Label(content_frame, text="Dodaj szafkę", **MAIN_LABEL_STYLE)
    title.pack(pady=20)

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
    locker_room = Combobox(locker_details_frame, values=["Szkoła Podstawowa", "Liceum"], state="readonly",**COMBOBOX_STYLE)
    locker_room.grid(row=1, column=0, padx=5, columnspan=2)
    locker_room.current(0)

    # ROW
    locker_row_label = Label(locker_details_frame, text="Rząd", **LABEL_STYLE)
    locker_row_label.grid(row=0, column=2, padx=5, pady=10, sticky="n", columnspan=2)
    locker_row = Entry(locker_details_frame, **ENTRY_STYLE)
    locker_row.grid(row=1, column=2, padx=5,  columnspan=2)

    # Column
    locker_column_label = Label(locker_details_frame, text="Kolumna", **LABEL_STYLE)
    locker_column_label.grid(row=0, column=4, padx=5, pady=10, sticky="n", columnspan=2)
    locker_column = Entry(locker_details_frame, **ENTRY_STYLE)
    locker_column.grid(row=1, column=4, padx=5, columnspan=2)



    def add_locker_action():
        try:
            if locker_nr.get() == ""  or locker_row.get() == "" or locker_column.get() == "":
                messagebox.showwarning("Brak danych", "Nie podano wszystkich danych.")
                return

            for l in lockersList:
                if l.number == int(locker_nr.get()):
                    if l.room == locker_room.get() and l.position == (int(locker_row.get()), int(locker_column.get())):
                        messagebox.showerror("Błąd", "Szafka o podanym numerze już istnieje.")
                        return
                    else:
                        l.room = locker_room.get()
                        l.position = (int(locker_row.get()), int(locker_column.get()))
                        # update db posiotion
                        update_locker_position_in_db(l)
                        # refresh listbox
                        locker_listbox.delete(0, END)
                        for l in lockersList:
                            locker_listbox.insert(END, str(l))
                        return
                if l.room == locker_room.get() and l.position == (int(locker_row.get()), int(locker_column.get())):
                    messagebox.showerror("Błąd", "Szafka o takim połozeniu już istnieje.")
                    return


            number = int(locker_nr.get())
            room = locker_room.get()
            row = int(locker_row.get())
            column = int(locker_column.get())

            locker = Locker(number, room, row, column, False)
            # adding to list
            lockersList.append(locker)
            # adding to listbox
            locker_listbox.insert(END, str(locker))
            # adding to db
            add_locker_to_db(locker)
        except ValueError:
            messagebox.showerror("Błąd", "Numer szafki, rząd i kolumna muszą być liczbami całkowitymi.")
            return
        except Exception as e:
            messagebox.showerror("Błąd", f"{e}")
            return


    locker_button = Button(content_frame, text="Dodaj szafkę", **BUTTON_STYLE,command=add_locker_action)
    locker_button.pack(pady=20)


    locker_list_label = Label(content_frame, text="Lista szafek", **MAIN_LABEL_STYLE)
    locker_list_label.pack(pady=20)

    locker_listbox = Listbox(content_frame, **LISTBOX_STYLE)
    locker_listbox.pack(fill=BOTH, expand=True, padx=20)
    mainPage.update()

    # displaying all  lockers on listbox
    for l in lockersList:
        locker_listbox.insert(END, str(l))


# Dodaj klase
def add_class():
    mainPage.update()
    clear_frame()
    back_btn = button_back()
    back_btn.place(x=10, y=10)
    title = Label(content_frame, text="Dodaj klase", **MAIN_LABEL_STYLE)
    title.pack(pady=20)

    class_name_label = Label(content_frame, text="Nazwa klasy", **LABEL_STYLE)
    class_name_label.pack(pady=10)
    class_name = Entry(content_frame, **ENTRY_STYLE)
    class_name.pack()

    class_number_label = Label(content_frame, text="Liczba uczniow w klasie", **LABEL_STYLE)
    class_number_label.pack(pady=10)
    class_number = Entry(content_frame, **ENTRY_STYLE)
    class_number.pack()

    # on button click add class to list
    def add_class_action():
        if class_name.get() == "" or class_number.get() == "":
            messagebox.showwarning("Brak danych", "Nie podano wszystkich danych.")
            return
        if not re.match("^[0-9][A-Z]$", class_name.get()):
            messagebox.showerror("Błąd", "Nazwa musi sie skladac z cyfry i dużej litery. np 1A, 2B.")
            return
        for c in classList:
            if c.name == class_name.get():
                if c.number_of_students== int(class_number.get()):
                    messagebox.showerror("Błąd", "Klasa o podanej nazwie i liczbie uczniów już istnieje.")
                    return
                else:
                    c.number_of_students = int(class_number.get())
                    update_class_in_db(c)
                    class_listbox.delete(0, END)
                    for c in classList:
                        class_listbox.insert(END, str(c))
                    return

        if int(class_number.get()) < 0:
            messagebox.showerror("Błąd", "Liczba uczniów w klasie nie może być ujemna.")
            return
        try:
            name = class_name.get()
            number = int(class_number.get())
            school_class = Class(name, number)
            # adding to list
            classList.append(school_class)
            # adding to listbox
            class_listbox.insert(END, str(school_class))
            # adding to db
            add_class_to_db(school_class)
        except ValueError:
            messagebox.showerror("Błąd", "Liczba uczniów w klasie musi być liczbą całkowitą.")
            return
        except Exception as e:
            messagebox.showerror("Błąd", f"{e}")
            return

    class_button = Button(content_frame, text="Dodaj klase", **BUTTON_STYLE, command=add_class_action)
    class_button.pack(pady=20)

    class_listbox = Listbox(content_frame, **LISTBOX_STYLE)
    class_listbox.pack(fill=BOTH, expand=True, padx=20, pady=20)

    # displaying all  school classes on listbox
    for c in classList:
        class_listbox.insert(END, str(c))
    mainPage.update()




# Main window
def main():
    mainPage.update()
    clear_frame()
    tytul = Label(content_frame, text="Menadżer kluczy", **MAIN_LABEL_STYLE)
    tytul.pack(pady=20)

    # Frame for buttons
    button_frame = Frame(content_frame, **FRAME_STYLE)
    button_frame.pack(fill=X, pady=20)

    buttons = [
        ("Dodaj klucz", add_key),
        ("Dodaj szafkę", add_locker),
        ("Dodaj klase", add_class)
    ]

    for text, command in buttons:
        buttons=Button(button_frame, text=text, **BUTTON_STYLE, command=command)
        buttons.pack(side=LEFT,fill=BOTH,expand=True, padx=10)


    error_label = Label(content_frame, text="Błędy", **MAIN_LABEL_STYLE)
    error_label.pack(pady=20)
    #listbox
    erors_listbox = Listbox(content_frame, **LISTBOX_STYLE)
    erors_listbox.pack(fill=BOTH, expand=True, padx=20)

    # displaying all lockers with no keys assigned and keys witch no class assigned
    for l in lockersList:
        if not l.key_assigned:
            erors_listbox.insert(END, str(l.display_if_key_not_assigned()))
    for k in keysList:
        if k.keyclass == "Brak":
            erors_listbox.insert(END, str(k.display_if_not_assigned()))

    mainPage.update()



# Główna pętla aplikacji
if __name__ == "__main__":
    create_db()
    classList, keysList, lockersList = import_from_db_to_lists(classList, keysList, lockersList)
    main()
    mainPage.mainloop()

