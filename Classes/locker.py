class Locker():
    id=0
    def __init__(self, number:int,room:str,row:int,column:int):
        Locker.id+=1
        self.__number=number
        self.__position=(room,row,column)

    def changePosition(self,room,row,column):
        self.__position=(room,row,column)


