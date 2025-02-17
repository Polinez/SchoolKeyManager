# tkinter
from tkinter import *
from tkinter.ttk import Combobox

# Database
from dataBase.data import *

# styles
from styles import *

# actions
from actions import keys_actions
from actions import lockers_actions
from actions import class_actions
from actions import main_actions

# lists
from lists import classList, keysList, lockersList



def clear_frame():
    for widget in content_frame.winfo_children():
        widget.destroy()


def button_back():
    return Button(content_frame,text="Wróć",**BUTTON_STYLE,command=main)



# Functions for adding keys, lockers and classes

def add_key():
    mainPage.update()
    clear_frame()

    back_btn = button_back()
    back_btn.place(x=10, y=10)

    title = Label(content_frame, text="Dodaj/Edytuj klucz", **MAIN_LABEL_STYLE)
    title.pack(pady=20)


    find_locker_btn = Button(content_frame, text="Znajdz klucz", **BUTTON_STYLE, command=lambda :keys_actions.find_key_action(key_nr))
    find_locker_btn.pack(pady=10)
    mainPage.update()
    # changing position of find locker button after window update because it broke when we do it before
    find_locker_btn.place(x=mainPage.winfo_width() - find_locker_btn.winfo_width() -10, y=10)

    key_nr_lb = Label(content_frame, text="Numer klucza", **LABEL_STYLE)
    key_nr_lb.pack(pady=10)
    key_nr = Entry(content_frame, **ENTRY_STYLE)
    key_nr.pack()

    key_class_lb = Label(content_frame, text="Przypisz do klasy", **LABEL_STYLE)
    key_class_lb.pack(pady=10)
    key_class = Combobox(content_frame, values=["Koszyk"]+[c.name for c in classList], state="readonly", **COMBOBOX_STYLE)
    key_class.pack()
    key_class.current(0)


    key_button = Button(content_frame, text="Dodaj klucz", **BUTTON_STYLE, command=lambda :keys_actions.add_key_action(key_nr, key_class, key_table))
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


    # refreshing keys table
    mainPage.update()
    keys_actions.refresh_key_table(key_table)




def add_locker():
    mainPage.update()
    clear_frame()

    back_btn = button_back()
    back_btn.place(x=10, y=10)
    title = Label(content_frame, text="Dodaj/Edytuj szafkę", **MAIN_LABEL_STYLE)
    title.pack(pady=20)


    find_locker_btn = Button(content_frame, text="Znajdz szafke", **BUTTON_STYLE, command=lambda :lockers_actions.find_locker_action(locker_nr))
    find_locker_btn.pack(pady=10)
    # changing position of find locker button after window update because it broke when we do it before
    mainPage.update()
    find_locker_btn.place(x=mainPage.winfo_width() - find_locker_btn.winfo_width() -10, y=10)

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
    locker_row = Combobox(locker_details_frame, values=["Góra", "Dół"], state="readonly", **COMBOBOX_STYLE)
    locker_row.grid(row=1, column=2, padx=5,  columnspan=2)
    locker_row.current(0)

    # Column
    locker_column_label = Label(locker_details_frame, text="Kolumna", **LABEL_STYLE)
    locker_column_label.grid(row=0, column=4, padx=5, pady=10, sticky="n", columnspan=2)
    locker_column = Entry(locker_details_frame, **ENTRY_STYLE)
    locker_column.grid(row=1, column=4, padx=5, columnspan=2)


    locker_button = Button(content_frame, text="Dodaj szafkę", **BUTTON_STYLE,
                           command=lambda : lockers_actions.add_locker_action( locker_nr,locker_room, locker_row, locker_column, locker_table))
    locker_button.pack(pady=20)

    locker_list_label = Label(content_frame, text="Lista szafek", **MAIN_LABEL_STYLE)
    locker_list_label.pack()


    save_lockers_btn = Button(content_frame, text="Zapisz szafki do PDF", **BUTTON_STYLE,command=lockers_actions.save_lockers_action)
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


    mainPage.update()
    lockers_actions.refresh_locker_table(locker_table)


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


    class_button = Button(content_frame, text="Dodaj klasę", **BUTTON_STYLE, command=lambda :class_actions.add_class_action(class_name, class_number, class_table))
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


    mainPage.update()
    class_actions.refresh_class_table(class_table)



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


    save_key = Button(content_frame, text="Zapisz", **BUTTON_STYLE, command=lambda: keys_actions.save_keys_action(class_name))
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


def change_locker():
    mainPage.update()
    clear_frame()

    # Przycisk powrotu
    back_btn = button_back()
    back_btn.place(x=10, y=10)

    # Tytuł
    title = Label(content_frame, text="Zmień zamek w szafce", **MAIN_LABEL_STYLE)
    title.pack(pady=20)

    # buttons frame
    buttons_frame = Frame(content_frame, **FRAME_STYLE)
    buttons_frame.pack(pady=20)

    # locker 1 frame
    buton1_frame = Frame(buttons_frame, **FRAME_STYLE)
    buton1_frame.pack(side=LEFT, padx=20)
    # locker 2 frame
    buton2_frame = Frame(buttons_frame, **FRAME_STYLE)
    buton2_frame.pack(side=LEFT, padx=20)


    # Elements of locker 1 frame
    old_locker_label = Label(buton1_frame, text="STARY numer szafki", **LABEL_STYLE)
    old_locker_label.pack(pady=10)

    old_locker_nr = Entry(buton1_frame, **ENTRY_STYLE)
    old_locker_nr.pack()

    # Elements of locker 2 frame
    new_locker_label = Label(buton2_frame, text="NOWY numer szafki", **LABEL_STYLE)
    new_locker_label.pack(pady=10)

    new_locker_nr = Entry(buton2_frame, **ENTRY_STYLE)
    new_locker_nr.pack()


    # Elements of locker position
    locker_room_label = Label(content_frame, text="Sala", **LABEL_STYLE)
    locker_room_label.pack(pady=10)

    locker_room = Combobox(content_frame, values=["Szkoła Podstawowa", "Liceum"], state="readonly", **COMBOBOX_STYLE)
    locker_room.pack()
    locker_room.current(0)

    locker_row_label = Label(content_frame, text="Rząd", **LABEL_STYLE)
    locker_row_label.pack(pady=10)

    locker_row = Combobox(content_frame, values=["Góra", "Dół"], state="readonly", **COMBOBOX_STYLE)
    locker_row.pack()
    locker_row.current(0)

    locker_column_label = Label(content_frame, text="Kolumna", **LABEL_STYLE)
    locker_column_label.pack(pady=10)

    locker_column = Entry(content_frame, **ENTRY_STYLE)
    locker_column.pack()


    change_locker_btn = Button(content_frame, text="Zmień zamek", **BUTTON_STYLE, command=lambda: lockers_actions.change_locker_nr_action(old_locker_nr, new_locker_nr, locker_room, locker_row, locker_column))
    change_locker_btn.pack(pady=20)

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
        ("Zapisz klucze", save_keys),
        ("Zmień zamek", change_locker)
    ]

    for text, command in buttons:
        button = Button(button_frame, text=text, **BUTTON_STYLE, command=command)
        button.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

    error_label = Label(content_frame, text="Błędy", **MAIN_LABEL_STYLE)
    error_label.pack()

    save_errors_btn = Button(content_frame, text="Zapisz błędy", **BUTTON_STYLE, command=main_actions.save_errors_action)
    save_errors_btn.pack(pady=10)

    # Treeview for errors
    error_table = Treeview(content_frame, columns=("Typ", "Wiadomość"), show="headings", )
    error_table.pack(fill=BOTH, expand=True, padx=20)

    # Define columns and their headings
    error_table.heading("Typ", text="Typ")
    error_table.heading("Wiadomość", text="Wiadomość")

    # Adjust column width
    error_table.column("Typ", width=80)
    error_table.column("Wiadomość", width=800)


    main_actions.refresh_error_table(error_table)

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

    # checking version
    main_actions.check_for_update()
    # Create database
    create_db()
    # Run
    main()
    mainPage.mainloop()

