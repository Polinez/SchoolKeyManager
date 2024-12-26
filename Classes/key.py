class Key():
    id=0
    def __init__(self, keysNr:int,status:str):
        Key.id+=1
        self.__keysNr=keysNr
        self.__status=status

    def changeStatus(self):
        if self.__status=="wolny":
            self.__status="zajety"
        else:
            self.__status="wolny"