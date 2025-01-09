from tkinter import messagebox
from fpdf import FPDF

from dataBase.data import delete_key_from_db, update_locker_status_in_db, delete_locker_from_db, delete_class_from_db,import_from_db_to_lists



# saves keys to pdf
def save_keys_action(selected_class):
    classList, keysList, lockersList = import_from_db_to_lists()
    if selected_class == "Wszystkie":
        keys = keysList
    else:
        keys = [k for k in keysList if k.keyclass == selected_class]

    if not keys:
        messagebox.showinfo("Info", "Brak kluczy do zapisu.")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Lista Kluczy", ln=True, align='C')
    pdf.ln(10)  # line break

    for key in keys:
        pdf.cell(0, 10, txt=f"Klucz: {key.number}, Przypisany do klasy: {key.keyclass}", ln=True)

    try:
        pdf_file = "klucze.pdf"
        pdf.output(pdf_file)
        messagebox.showinfo("Info",
                        f"Klucze zostały zapisane do pliku {pdf_file} w folderze aplikacji. \nMożesz teraz je wydrukować.")
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas zapisu pliku PDF: {e}")



# Deleting actions
def delete_key_action(key_number:str):
    classList, keysList, lockersList = import_from_db_to_lists()
    if not key_number.isdigit():
        messagebox.showerror("Error", "Podaj numer klucza jako liczbe")
        return

    key_number = int(key_number)
    key_to_delete = None

    #find key to delete
    for key in keysList:
        if key.number == key_number:
            key_to_delete = key
            break

    if key_to_delete is None:
        messagebox.showerror("Error", f"Nie ma klucza nr {key_number}. Wpisz numer klucza z listy")
        return

    # deleting key
    keysList.remove(key_to_delete)
    delete_key_from_db(key_to_delete)

    # change locker status
    for locker in lockersList:
        if locker.number == key_to_delete.number:
            locker.key_assigned = False
            update_locker_status_in_db(locker)
            messagebox.showinfo("Info", f"Zmieniono status szafki nr {locker.number}")
            break

    messagebox.showinfo("Info", f"Usunięto klucz nr {key_number}")




def delete_locker_action(locker_number:str):
    classList, keysList, lockersList = import_from_db_to_lists()
    if not locker_number.isdigit():
        messagebox.showerror("Error", "Podaj numer szafki jako liczbe")
        return

    locker_number = int(locker_number)
    locker_to_delete = None

    # find locker to delete
    for locker in lockersList:
        if locker.number == locker_number:
            locker_to_delete = locker
            break

    if locker_to_delete is None:
        messagebox.showerror("Error", f"Nie ma szafki nr {locker_number}. Wpisz numer szafki z listy")
        return

    # deleting locker
    lockersList.remove(locker_to_delete)
    delete_locker_from_db(locker_to_delete)
    messagebox.showinfo("Info", f"Usunięto szafkę nr {locker_number}")


def delete_class_action(class_name:str):
    classList, keysList, lockersList = import_from_db_to_lists()

    class_to_delete = None

    # find class to delete
    for schoolClass in classList:
        if schoolClass.name == class_name:
            class_to_delete = schoolClass
            break

    if not class_to_delete:
        messagebox.showerror("Error", f"Nie ma klasy {class_name}. Wpisz nazwę klasy z listy")
        return

    # check if class has key
    for key in keysList:
        if key.keyclass == class_name:
            messagebox.showerror("Error", f"Nie można usunąć klasy {class_name} ponieważ ma ona przypisany klucz")
            return

    # deleting class
    classList.remove(class_to_delete)
    delete_class_from_db(class_to_delete)
    messagebox.showinfo("Info", f"Usunięto klasę {class_name}")
