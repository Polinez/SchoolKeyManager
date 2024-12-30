class Locker():
    id=0
    def __init__(self, number:int,room:str,row:str,column:int,key_assigned:bool):
        Locker.id+=1
        self.__ID = Locker.id
        self.__number=number
        self.__room=room
        self.__position=(row,column)
        self.__key_assigned=key_assigned

    def __str__(self):
        return f"{self.__ID}.\t nr:{self.__number}\t pokoj:{self.__room}\t pozycja:{self.__position}\t" + (" klucz: Przydzielony" if self.__key_assigned else f" klucz: Nie przydzielony")

    def __eq__(self, other):
        return self.__ID == other.ID

    def display_if_key_not_assigned(self):
        return (f"Szafka nr {self.__number} w  {self.__room} o pozycji {self.__position} nie ma przydzielonego klucza.")

    def changePosition(self,room:str,row:str,column:int):
        self.__room=room
        self.__position=(row,column)



    @property
    def ID(self):
        return self.__ID

    @property
    def number(self):
        return self.__number

    @property
    def room(self):
        return self.__room

    @room.setter
    def room(self,room):
        self.__room=room

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self,position):
        self.__position=position

    @property
    def key_assigned(self):
        return self.__key_assigned

    @key_assigned.setter
    def key_assigned(self,key_assigned):
        self.__key_assigned=key_assigned

