import uuid


class Employee:

    def __init__(self, ID, name, surname, bindedCard):
        self.ID = ID
        self.name = name
        self.surname = surname
        self.bindedCard = bindedCard

    def bindCard(self, CID):
        self.bindedCard = CID

    def toString(self):
        return ("""{} 
        {} 
        {} 
        {} 
        {}""".format(self.ID, self.name, self.surname, self.bindedCard, self.checkedIn))
