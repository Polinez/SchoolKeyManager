import re

class Class:
    id=0
    def __init__(self, class_name,number_of_students):
        if not re.match(r'^[1-9][A-Z]$', class_name):
            raise ValueError("Nazwa klasy musi składać się z cyfry i wielkiej litery, np. 1A, 2B, itp.")
        Class.id+=1
        self.__ID = Class.id
        self.__className = class_name
        self.__numberOfStudents = number_of_students

    def __str__(self):
        return f"{self.__ID}. {self.__className}, ilosc uczniow:{self.__numberOfStudents}"


    @property
    def name(self):
        return self.__className


    @property
    def number_of_students(self):
        return self.__numberOfStudents



