# tkinter
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
# Database
from dataBase.data import *
# objects
from classes.key import Key
from classes.schoolClass import Class
from classes.locker import Locker


# Main window config
mainPage = Tk()
mainPage.title("Menadżer kluczy")
mainPage.geometry("820x640")
mainPage.configure(bg="white")
mainPage.resizable(False, False)

# main frame to hold all content
content_frame = Frame(mainPage, bg="black")
content_frame.pack(fill=BOTH, expand=True)

# Lists of objects
keysList = []
classList = []
lockersList = []



def clear_frame():
    for widget in content_frame.winfo_children():
        widget.destroy()


def button_back():
    return Button(content_frame,text="Wróć",bg="white",fg="black",font=("Arial", 16),command=main)

# Funkcje dla poszczególnych opcji menu

# Dodaj klucz
def add_key():
    mainPage.update()
    clear_frame()
    back_btn = button_back()
    back_btn.place(x=10, y=10)
    title = Label(content_frame, text="Dodaj klucz", bg="black", fg="white", font=("Arial", 24))
    title.pack(pady=20)

    key_lb = Label(content_frame, text="Numer klucza", bg="black", fg="white", font=("Arial", 16))
    key_lb.pack(pady=10)
    key_nr = Entry(content_frame, bg="white", fg="black", font=("Arial", 16))
    key_nr.pack()

    status_lb = Label(content_frame, text="Status klucza", bg="black", fg="white", font=("Arial", 16))
    status_lb.pack(pady=10)
    status = Combobox(content_frame, values=["Wypożyczony", "Dostępny"], state="readonly", font=("Arial", 16))
    status.pack()
    status.current(1)


    def add_key_action():
        if key_nr.get() == "":
            messagebox.showwarning("Brak danych", "Nie podano wszystkich danych.")
            return
        try:
            key_number = int(key_nr.get())
        except ValueError:
            messagebox.showerror("Błąd", "Numer klucza musi być liczbą całkowitą.")
            return
        key_status = status.get()
        key = Key(key_number, key_status)
        messagebox.showinfo("Sukces", f"Stworzono klucz o numerze {key_number} i statusie {key_status}")
        keysList.append(key)

    # Przyciski
    key_button = Button(content_frame, text="Dodaj klucz", bg="white", fg="black", font=("Arial", 16),command=add_key_action)
    key_button.pack(pady=20)



# Dodaj szafkę
def add_locker():
    mainPage.update()
    clear_frame()
    back_btn = button_back()
    back_btn.place(x=10, y=10)
    title = Label(content_frame, text="Dodaj szafkę", bg="black", fg="white", font=("Arial", 24))
    title.pack(pady=20)

    locker_nr_label = Label(content_frame, text="Numer szafki", bg="black", fg="white", font=("Arial", 16))
    locker_nr_label.pack(pady=10)
    locker_nr = Entry(content_frame, bg="white", fg="black", font=("Arial", 16))
    locker_nr.pack()

    locker_room_label = Label(content_frame, text="Sala", bg="black", fg="white", font=("Arial", 16))
    locker_room_label.pack(pady=10)
    locker_room = Combobox(content_frame, values=["Szkoła Podstawowa","Liceum"], state="readonly", font=("Arial", 16))
    locker_room.pack()
    locker_room.current(0)

    locker_row_label = Label(content_frame, text="Rząd", bg="black", fg="white", font=("Arial", 16))
    locker_row_label.pack(pady=10)
    locker_row = Entry(content_frame, bg="white", fg="black", font=("Arial", 16))
    locker_row.pack()

    locker_column_label = Label(content_frame, text="Kolumna", bg="black", fg="white", font=("Arial", 16))
    locker_column_label.pack(pady=10)
    locker_column = Entry(content_frame, bg="white", fg="black", font=("Arial", 16))
    locker_column.pack()

    locker_status_label = Label(content_frame, text="Status szafki", bg="black", fg="white", font=("Arial", 16))
    locker_status_label.pack(pady=10)
    locker_status = Combobox(content_frame, values=["Wolna", "Zajęta"], state="readonly", font=("Arial", 16))
    locker_status.pack()
    locker_status.current(0)


    def add_locker_action():
        if locker_nr.get() == ""  or locker_row.get() == "" or locker_column.get() == "":
            messagebox.showwarning("Brak danych", "Nie podano wszystkich danych.")
            return
        for l in lockersList:
            if l.number == int(locker_nr.get()):
                messagebox.showerror("Błąd", "Szafka o podanym numerze już istnieje.")
                return
        try:
            number = int(locker_nr.get())
            room = locker_room.get()
            row = int(locker_row.get())
            column = int(locker_column.get())
            status = locker_status.get()

            locker = Locker(number, room, row, column, status)
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


    locker_button = Button(content_frame, text="Dodaj szafkę", bg="white", fg="black", font=("Arial", 16),command=add_locker_action)
    locker_button.pack(pady=20)

    locker_listbox = Listbox(content_frame, bg="white", fg="black", font=("Arial", 16), selectbackground="white", selectforeground="black")
    locker_listbox.pack(fill=BOTH, expand=True, padx=20, pady=20)

    # displaying all  lockers on listbox
    for l in lockersList:
        locker_listbox.insert(END, str(l))

# Dodaj klase
def add_class():
    mainPage.update()
    clear_frame()
    back_btn = button_back()
    back_btn.place(x=10, y=10)
    title = Label(content_frame, text="Dodaj klase", bg="black", fg="white", font=("Arial", 24))
    title.pack(pady=20)

    class_name_label = Label(content_frame, text="Nazwa klasy", bg="black", fg="white", font=("Arial", 16))
    class_name_label.pack(pady=10)
    class_name = Entry(content_frame, bg="white", fg="black", font=("Arial", 16))
    class_name.pack()

    class_number_label = Label(content_frame, text="Liczba uczniow w klasie", bg="black", fg="white", font=("Arial", 16))
    class_number_label.pack(pady=10)
    class_number = Entry(content_frame, bg="white", fg="black", font=("Arial", 16))
    class_number.pack()

    # on button click add class to list
    def add_class_action():
        if class_name.get() == "" or class_number.get() == "":
            messagebox.showwarning("Brak danych", "Nie podano wszystkich danych.")
            return
        for c in classList:
            if c.name == class_name.get():
                messagebox.showerror("Błąd", "Klasa o podanej nazwie już istnieje.")
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

    class_button = Button(content_frame, text="Dodaj klase", bg="white", fg="black", font=("Arial", 16),command=add_class_action)
    class_button.pack(pady=20)

    class_listbox = Listbox(content_frame, bg="white", fg="black", font=("Arial", 16), selectbackground="white", selectforeground="black")
    class_listbox.pack(fill=BOTH, expand=True, padx=20, pady=20)

    # displaying all  school classes on listbox
    for c in classList:
        class_listbox.insert(END, str(c))
    mainPage.update()



# Przypisz klucz
def assign_key():
    clear_frame()
    back_btn = button_back()
    back_btn.place(x=10, y=10)
    title = Label(content_frame, text="Przypisz klucz", bg="black", fg="white", font=("Arial", 24))
    title.pack(pady=20)


# Main window
def main():
    mainPage.update()
    clear_frame()
    tytul = Label(content_frame, text="Menadżer kluczy", bg="black", fg="white", font=("Arial", 24))
    tytul.pack(pady=20)

    # Frame for buttons
    button_frame = Frame(content_frame, bg="black")
    button_frame.pack(fill=X, pady=20)

    buttons = [
        ("Dodaj klucz", add_key),
        ("Dodaj szafkę", add_locker),
        ("Dodaj klase", add_class),
        ("Przypisz klucz", assign_key)
    ]

    for text, command in buttons:
        Button(button_frame, text=text, bg="white", fg="black", font=("Arial", 16), command=command).pack(side=LEFT,fill=BOTH,expand=True, padx=10)

    #listbox
    assign_key_listbox = Listbox(content_frame, bg="white", fg="black", font=("Arial", 16), selectbackground="white", selectforeground="black")
    assign_key_listbox.pack(fill=BOTH, expand=True, padx=20, pady=20)



# Główna pętla aplikacji
if __name__ == "__main__":
    create_db()
    classList,keysList,lockersList=import_from_db_to_lists(classList, keysList, lockersList)
    main()
    mainPage.mainloop()

