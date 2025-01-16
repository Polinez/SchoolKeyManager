from tkinter import messagebox
from fpdf import FPDF
from dataBase.data import import_from_db_to_lists
from unidecode import unidecode

# import lists from database
classList, keysList, lockersList = import_from_db_to_lists()

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
            pdf.cell(0, 4, f"Klucz: {key.number}, Przypisany do klasy: {key.keyclass}", new_x="LMARGIN", new_y="NEXT")

        try:
            pdf_file = "klucze.pdf"
            pdf.output(pdf_file)
            messagebox.showinfo("Info",
                                f"Klucze zostały zapisane do pliku {pdf_file} w folderze aplikacji. \nMożesz teraz je wydrukować.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas zapisu pliku PDF: {e}")