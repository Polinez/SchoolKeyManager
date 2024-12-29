
# Deleting actions
def delete_key_action(nr_klucza:str,list_of_keys:list):
    # TODO: usuniecie klucza usuwa klucz z listy i z bazy oraz status szafki zmieniamy na "Wolna"
    nr_klucza=int(nr_klucza)
    if nr_klucza not in list_of_keys:
        print("Nie ma takiego klucza")
        print(nr_klucza)
        print(list_of_keys)
    else:
        print(nr_klucza)
        print(list_of_keys)

def delete_locker_action(nr_szafki:str,list_of_lockers:list):
    # TODO: usuniecie szafki z listy i z bazy oraz blokada przed usunieciem przed usunieciem klucza przypisanego do szafki
    nr_szafki=int(nr_szafki)
    if nr_szafki not in list_of_lockers:
        print("Nie ma takiej szafki")
        print(nr_szafki)
        print(list_of_lockers)
    else:
        print(nr_szafki)
        print(list_of_lockers)

def delete_class_action(nazwa_klasy:str,list_of_classes:list):
    # TODO: usuniecie klasy z listy i z bazy ale zabezpieczyc przed usunieciem klasy ktora ma przypisany klucz
    if nazwa_klasy not in list_of_classes:
        print("Nie ma takiej klasy")
        print(nazwa_klasy)
        print(list_of_classes)
    else:
        print(nazwa_klasy)
        print(list_of_classes)