class Locker():
    id=0
    def __init__(self, number:int,room:str,row:int,column:int,status:str):
        Locker.id+=1
        self.__ID = Locker.id
        self.__number=number
        self.__room=room
        self.__position=(row,column)
        self.__status=status

    def __str__(self):
        return f"{self.__ID}.\t nr:{self.__number}\t pokoj:{self.__room}\t pozycja:{self.__position}\t status:{self.__status}"

    def changePosition(self,room,row,column):
        self.__room=room
        self.__position=(row,column)

    def changeStatus(self):
        if self.__status=="Wolna":
            self.__status="Zajęta"
        else:
            self.__status="Wolna"

    @property
    def number(self):
        return self.__number

    @property
    def room(self):
        return self.__room

    @property
    def position(self):
        return self.__position

    @property
    def status(self):
        return self.__status

