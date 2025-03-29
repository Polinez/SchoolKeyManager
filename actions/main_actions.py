import os.path
import sys
import threading
from tkinter import messagebox
import requests
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
        output_dir = "PDF"
        pdf_file = os.path.join(output_dir,"bledy.pdf")
        os.makedirs(output_dir, exist_ok=True)
        pdf.output(pdf_file)
        messagebox.showinfo("Info",
                            f"Bledy zostały zapisane do pliku {pdf_file} w folderze aplikacji. \nMożesz teraz je wydrukować.")
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas zapisu pliku PDF: {e}")



def get_version_file_path():
    if getattr(sys, 'frozen', False):
        # if app runs as EXE
        return os.path.join(sys._MEIPASS, 'version.txt')
    else:
        # if app runs in development environment
        return 'version.txt'

# check if there is no never version on github
def check_for_update(root):
    def check():
        try:
            url = "https://api.github.com/repos/Polinez/SchoolKeyManager/releases/latest"

            # Ustaw timeout (5 sekund na połączenie, 10 sekund na odpowiedź)
            response = requests.get(url, timeout=(5, 10))
            response.raise_for_status()

            latest_release = response.json()
            latest_version = latest_release['tag_name']
            release_url = latest_release['html_url']

            try:
                with open(get_version_file_path(), "r") as file:
                    local_version = file.read().strip()

                if local_version != latest_version:
                    root.after(0, lambda: messagebox.showinfo(
                        "Nowa wersja!",
                        f"Dostępna jest nowa wersja: {local_version} -> {latest_version}\n"
                        f"Zaktualizuj aplikację!\n\n"
                        f"Aby pobrać najnowszą wersję, odwiedź:\n{release_url}"
                    ))

            except FileNotFoundError:
                root.after(0, lambda: messagebox.showwarning(
                    "Błąd",
                    "Nie można znaleźć pliku wersji lokalnej."
                ))

        except requests.exceptions.Timeout:
            # Czas oczekiwania na odpowiedź przekroczony - pomijamy komunikat
            pass

        except requests.exceptions.ConnectionError:
            # Brak połączenia internetowego - również pomijamy komunikat
            pass

        except requests.exceptions.RequestException as e:
            # Inne błędy - logujemy, ale nie wyświetlamy użytkownikowi
            print(f"Błąd podczas sprawdzania aktualizacji: {e}")

    # Uruchom w tle
    threading.Thread(target=check, daemon=True).start()