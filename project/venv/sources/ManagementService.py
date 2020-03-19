import uuid
import sqlite3
from Employee import Employee
from Terminal import Terminal

class ManagementService:
    conn = sqlite3.connect('../database/company.db')
    c = conn.cursor()

    def createEmployee(self, name, surname):
        self.c.execute("INSERT INTO employees VALUES ('{}', '{}', '{}')".format(uuid.uuid1(), name, surname))
        self.conn.commit()

    def createCard(self):
        self.c.execute("INSERT INTO cards VALUES ('{}')".format(uuid.uuid1()))
        self.conn.commit()

    def createTerminal(self, address, server):
        generatedUID = uuid.uuid1()
        self.c.execute("INSERT INTO terminals VALUES ('{}', '{}')".format(generatedUID, address))
        self.conn.commit()
        return Terminal(generatedUID, address, server)

    def getAllEmployees(self):
        self.c.execute("SELECT * FROM employees")
        return self.c.fetchall()

    def getAllBindings(self):
        self.c.execute("SELECT * FROM bindings")
        return self.c.fetchall()

    def getAllCards(self):
        self.c.execute("SELECT * FROM cards")
        return self.c.fetchall()

    def getLogs(self):
        self.c.execute("SELECT * FROM logs")
        return self.c.fetchall()

    def printLogs(self):
        logs = self.getLogs()
        inc = 0
        for log in logs:
            print("{}: CardID: {} ; TerminalID: {} ; EmployeeID: {} ; Action: {} ; Date: {}".format(inc, log[0], log[1], log[2], log[3], log[4]))
            inc += 1
        inc = 0

    def printCards(self):
        cards = self.getAllCards()
        inc = 0
        for card in cards:
            print("{}: CardID: {}".format(inc, card[0]))
            inc += 1
        inc = 0

    def printAllEmployees(self):
        employees = self.getAllEmployees()
        inc = 0
        for emp in employees:
            print("{}: EmployeeID: {}, Name: {}, Surname: {}".format(inc, emp[0], emp[1], emp[2]))
            inc += 1
        inc = 0

    def deleteEmployee(self, EID):
        self.c.execute("DELETE FROM employees WHERE EID = '{}'".format(EID))

    def deleteCard(self, CID):
        self.c.execute("DELETE FROM cards WHERE CID = '{}'".format(CID))

    def getEmployeeById(self, EID):
        self.c.execute("SELECT * FROM employees WHERE EID='{}'".format(EID))
        employee = self.c.fetchone()
        if employee is None:
            print("There is no such employee")
            return
        self.c.execute("SELECT CID FROM bindings WHERE EID='{}'".format(EID))
        cards = self.c.fetchall()
        listOfCards = []
        for card in cards:
            listOfCards.append(card[0])
        return Employee(employee[0], employee[1], employee[2], listOfCards)

