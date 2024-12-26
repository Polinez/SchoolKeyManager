from tkinter import *
from Classes.key import Key
from Classes.student import Student
from Classes.locker import Locker

# Main window config
mainPage = Tk()
mainPage.title("Menadżer kluczy")
mainPage.geometry("820x640")
mainPage.configure(bg="black")
mainPage.resizable(False, False)

# main frame to hold all content
content_frame = Frame(mainPage, bg="black")
content_frame.pack(fill=BOTH, expand=True)

def clear_frame():
    for widget in content_frame.winfo_children():
        widget.destroy()

def show_main():
    clear_frame()
    tytul = Label(content_frame, text="Menadżer kluczy", bg="black", fg="white", font=("Arial", 24))
    tytul.pack(pady=20)

    # Frame for buttons
    button_frame = Frame(content_frame, bg="black")
    button_frame.pack(fill=X, pady=20)

    # Buttons in the button_frame, each will take 1/4 of the space
    add_key_button = Button(button_frame, text="Dodaj klucz", bg="white", fg="black", font=("Arial", 16),
                            command=add_key)
    add_key_button.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

    add_locker_button = Button(button_frame, text="Dodaj szafkę", bg="white", fg="black", font=("Arial", 16),
                               command=add_locker)
    add_locker_button.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

    add_student_button = Button(button_frame, text="Dodaj ucznia", bg="white", fg="black", font=("Arial", 16),
                                command=add_student)
    add_student_button.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

    assign_key_button = Button(button_frame, text="Przypisz klucz", bg="white", fg="black", font=("Arial", 16),
                               command=assign_key)
    assign_key_button.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

#listbox
    assign_key_listbox = Listbox(content_frame, bg="black", fg="white", font=("Arial", 16), selectbackground="white", selectforeground="black")
    assign_key_listbox.pack(fill=BOTH, expand=True, padx=20, pady=20)

def button_back():
    return Button(content_frame,
                  text="Wróć",
                  bg="white",
                  fg="black",
                  font=("Arial", 16),
                  command=show_main
                  )

# Funkcje dla poszczególnych opcji menu
def add_key():
    clear_frame()
    bBack = button_back()
    bBack.place(x=10, y=10)
    title = Label(content_frame, text="Dodaj klucz", bg="black", fg="white", font=("Arial", 24))
    title.pack(pady=20)


    keyLabel = Label(content_frame, text="Numer klucza", bg="black", fg="white", font=("Arial", 16))
    keyLabel.pack(pady=10)
    keyNr = Entry(content_frame, bg="white", fg="black", font=("Arial", 16))
    keyNr.pack()

    statusLabel = Label(content_frame, text="Status klucza", bg="black", fg="white", font=("Arial", 16))
    statusLabel.pack(pady=10)
    status = Entry(content_frame, bg="white", fg="black", font=("Arial", 16))
    status.pack()

    key = Key(keyNr, status)

def add_locker():
    clear_frame()
    bBack = button_back()
    bBack.place(x=10, y=10)
    title = Label(content_frame, text="Dodaj szafkę", bg="black", fg="white", font=("Arial", 24))
    title.pack(pady=20)

def add_student():
    clear_frame()
    bBack = button_back()
    bBack.place(x=10, y=10)
    title = Label(content_frame, text="Dodaj ucznia", bg="black", fg="white", font=("Arial", 24))
    title.pack(pady=20)

def assign_key():
    clear_frame()
    bBack = button_back()
    bBack.place(x=10, y=10)
    title = Label(content_frame, text="Przypisz klucz", bg="black", fg="white", font=("Arial", 24))
    title.pack(pady=20)





# Główna pętla aplikacji
show_main()
mainPage.mainloop()
