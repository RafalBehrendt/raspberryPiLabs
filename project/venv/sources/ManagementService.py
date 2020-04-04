import uuid
import sqlite3
from Employee import Employee
from Terminal import Terminal
from DBManage import *


class ManagementService:
    conn = sqlite3.connect('../database/company.db')
    c = conn.cursor()

    def createEmployee(self, name, surname):
        generatedUUID = uuid.uuid1()
        self.c.execute("INSERT INTO employees VALUES ('{}', '{}', '{}')".format(generatedUUID, name, surname))
        self.conn.commit()

    def createCard(self):
        generatedUUID = uuid.uuid1()
        self.c.execute("INSERT INTO cards VALUES ('{}', 0, '{}')".format(generatedUUID, None))
        self.conn.commit()
        return generatedUUID

    def registerCard(self, CID):
        self.c.execute("UPDATE cards SET isRegistered = 1 WHERE CID = '{}'".format(CID))
        self.conn.commit()

    def createTerminal(self, address):
        generatedUUID = uuid.uuid1()
        self.c.execute("INSERT INTO terminals VALUES ('{}', '{}', '0')".format(generatedUUID, address))
        self.conn.commit()
        return Terminal(generatedUUID, address)

    def createTerminal(self, address, TID):
        self.c.execute("INSERT INTO terminals VALUES ('{}', '{}', '0')".format(TID, address))
        self.conn.commit()

    def getAllEmployees(self):
        self.c.execute("SELECT * FROM employees")
        return self.c.fetchall()

    def getAllBindings(self):
        self.c.execute("SELECT CID FROM cards WHERE EID IS NOT NULL")
        return self.c.fetchall()

    def getAllCards(self):
        self.c.execute("SELECT * FROM cards")
        return self.c.fetchall()

    def getAllTerminals(self):
        self.c.execute("SELECT * FROM terminals")
        return self.c.fetchall()

    def getLogs(self):
        self.c.execute("SELECT * FROM logs")
        return self.c.fetchall()

    def printLogs(self):
        logs = self.getLogs()
        inc = 0
        for log in logs:
            print("{}: CardID: {} ; TerminalID: {} ; EmployeeID: {} ; Action: {} ; Date: {}".format(inc, log[0], log[1],
                                                                                                    log[2], log[3],
                                                                                                    log[4]))
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

    def printAllTerminals(self):
        terminals = self.getAllTerminals()
        inc = 0
        for term in terminals:
            print("{}: TerminalID: {}, Address: {}".format(inc, term[0], term[1]))
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
        self.c.execute("SELECT CID FROM cards WHERE EID='{}'".format(EID))
        cards = self.c.fetchall()
        listOfCards = []
        for card in cards:
            listOfCards.append(card[0])
        return Employee(employee[0], employee[1], employee[2], listOfCards)

    def dropDB(self):
        res = ""
        while res != "N" or res != "Y":
            res = input("You're about to drop whole database and create new one, proceed? [Y/N]: ")
            if (res == "Y"):
                resetDB()
                return True
            elif (res == "N"):
                return False

    def initDB(self):
        initializeDB()

    def mockData(self, server):

        self.createEmployee("Andrzej", "Kowalski")
        self.createEmployee("Zdzislaw", "Skrzynecki")
        self.createEmployee("Mariusz", "Pudzianowski")
        self.createEmployee("Dorian", "Kaczmarczyk")

        for i in range(1, 10):
            self.createCard()
            self.createTerminal("localhost")

        server.loadTerminals()
        server.loadCards()

