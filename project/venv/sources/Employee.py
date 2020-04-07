import uuid


class Employee:

    def __init__(self, ID, name, surname, boundCards):
        self.ID = ID
        self.name = name
        self.surname = surname
        self.boundCards = boundCards

    def toString(self):
        return ("EID: {}\nName: {}\nSurname: {}\nbindedCards: {}"
                .format(self.ID, self.name, self.surname, self.boundCards))
