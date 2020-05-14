import uuid

import Constants
from Employee import Employee
from Terminal import Terminal
from DBManage import *


class ManagementService:

    def createEmployee(self, name, surname):
        conn = sqlite3.connect(Constants.DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        generatedUUID = uuid.uuid1()
        c.execute("INSERT INTO employees VALUES ('{}', '{}', '{}')".format(generatedUUID, name, surname))
        conn.commit()
        conn.close()

    def createCard(self):
        conn = sqlite3.connect(Constants.DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        generatedUUID = uuid.uuid1()
        c.execute("INSERT INTO cards VALUES ('{}', 0, '{}')".format(generatedUUID, None))
        conn.commit()
        conn.close()
        return generatedUUID

    def createTerminal(self, address):
        conn = sqlite3.connect(Constants.DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        generatedUUID = uuid.uuid1()
        c.execute("INSERT INTO terminals VALUES ('{}', '{}', '0')".format(generatedUUID, address))
        conn.commit()
        conn.close()
        return Terminal(generatedUUID, address)

    def createTerminalWithTID(self, address, TID):
        conn = sqlite3.connect(Constants.DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("SELECT * FROM terminals WHERE TID='{}'".format(TID))
        terminal = c.fetchone()
        if terminal is None:
            c.execute("INSERT INTO terminals VALUES ('{}', '{}', '0')".format(TID, address))
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False

    def getAllEmployees(self):
        conn = sqlite3.connect(Constants.DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("SELECT * FROM employees")
        emps = c.fetchall()
        conn.close()
        return emps

    def getAllCards(self):
        conn = sqlite3.connect(Constants.DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("SELECT * FROM cards")
        cards = c.fetchall()
        conn.close()
        return cards

    def getAllTerminals(self):
        conn = sqlite3.connect(Constants.DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("SELECT * FROM terminals")
        terms = c.fetchall()
        conn.close()
        return terms

    def getLogs(self):
        conn = sqlite3.connect(Constants.DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("SELECT * FROM logs")
        logs = c.fetchall()
        conn.close()
        return logs

    def getEmployeeById(self, EID):
        conn = sqlite3.connect(Constants.DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("SELECT * FROM employees WHERE EID='{}'".format(EID))
        employee = c.fetchone()
        if employee is None:
            print("There is no such employee")
            conn.close()
            return
        c.execute("SELECT CID FROM cards WHERE EID='{}'".format(EID))
        cards = c.fetchall()
        listOfCards = []
        for card in cards:
            listOfCards.append(card[0])
        conn.close()
        return Employee(employee[0], employee[1], employee[2], listOfCards)

    def mockData(self, server):

        self.createEmployee("Andrzej", "Kowalski")
        self.createEmployee("Zdzislaw", "Skrzynecki")
        self.createEmployee("Mariusz", "Pudzianowski")
        self.createEmployee("Dorian", "Kaczmarczyk")

        for i in range(1, 10):
            self.createCard()
            tmp = self.createTerminal("rav")

        server.registerTerminal(tmp.TID)

        server.loadTerminals()
        server.loadCards()
