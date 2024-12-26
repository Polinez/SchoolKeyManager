class Student():
    id=0
    def __init__(self, firstName, secoundName,schoolClass):
        Student.id+=1
        self.__firstName = firstName
        self.__secoundName = secoundName
        self.__schoolClass = schoolClass


    def changeClass(self,schoolClass):
        self.__schoolClass=schoolClass