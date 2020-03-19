import uuid


class Employee:

    def __init__(self, ID, name, surname, bindedCards):
        self.ID = ID
        self.name = name
        self.surname = surname
        self.bindedCards = bindedCards

    def toString(self):
        return ("EID: {}\nName: {}\nSurname: {}\nbindedCards: {}"
                .format(self.ID, self.name, self.surname, self.bindedCards))
