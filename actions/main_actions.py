from tkinter import messagebox
# pdf
from fpdf import FPDF
from unidecode import unidecode
#lists
from lists import lockersList, keysList

# Displaying all lockers with no keys assigned and keys with no class assigned
def refresh_error_table(error_table):
    for item in error_table.get_children():
        error_table.delete(item)  # Remove existing entries

    for l in lockersList:
        if not l.key_assigned:
            error_table.insert("", "end", values=("Szafka", str(l.display_if_key_not_assigned())))

    for k in keysList:
        if k.keyclass == "Koszyk":
            error_table.insert("", "end", values=("Klucz", str(k.display_if_not_assigned())))


# saves errors to pdf
def save_errors_action():
    if not lockersList and not keysList:
        messagebox.showerror("Info", "Brak szafek lub kluczy do zapisu.")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    pdf.cell(200, 10, "Lista anomalii", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)  # line break

    # sorting by locker number
    lockers = sorted(lockersList, key=lambda x: x.number)
    # sorting by key number
    keys = sorted(keysList, key=lambda x: x.number)

    for locker in lockers:
        if not locker.key_assigned:
            locker_text = f"{locker.display_if_key_not_assigned()}"
            pdf.cell(0, 4, unidecode(locker_text), new_x="LMARGIN", new_y="NEXT")

    for key in keys:
        if key.keyclass == "Koszyk":
            key_text = f"{key.display_if_not_assigned()}"
            pdf.cell(0, 4, unidecode(key_text), new_x="LMARGIN", new_y="NEXT")

    try:
        pdf_file = "bledy.pdf"
        pdf.output(pdf_file)
        messagebox.showinfo("Info",
                            f"Bledy zostały zapisane do pliku {pdf_file} w folderze aplikacji. \nMożesz teraz je wydrukować.")
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas zapisu pliku PDF: {e}")