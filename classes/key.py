class Key:
    id=0
    def __init__(self, number:int,keyclass:str,status:str):
        Key.id+=1
        self.__ID=Key.id
        self.__number=number
        self.__keyclass=keyclass
        self.__status=status

    def __str__(self):
        return f"{self.__ID}.\t klucz:{self.__number},\t przypisany do:{self.__keyclass}\t status:{self.__status}"

    def __eq__(self, other):
        return self.__ID == other.ID

    def display_if_not_assigned(self):
        return f"Klucz oraz szafka nr:{self.__number} nie ma przydzielonej klasy."



    @property
    def ID(self):
        return self.__ID

    @property
    def number(self):
        return self.__number


    @property
    def keyclass(self):
        return self.__keyclass

    @keyclass.setter
    def keyclass(self,keyclass):
        self.__keyclass=keyclass

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self,status):
        self.__status=status