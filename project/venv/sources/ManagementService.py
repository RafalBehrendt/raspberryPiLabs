import uuid
from Employee import Employee
from Terminal import Terminal
from DBManage import *


class ManagementService:

    def createEmployee(self, name, surname):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        generatedUUID = uuid.uuid1()
        c.execute("INSERT INTO employees VALUES ('{}', '{}', '{}')".format(generatedUUID, name, surname))
        conn.commit()
        conn.close()

    def createCard(self):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        generatedUUID = uuid.uuid1()
        c.execute("INSERT INTO cards VALUES ('{}', 0, '{}')".format(generatedUUID, None))
        conn.commit()
        conn.close()
        return generatedUUID

    def registerCard(self, CID):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("UPDATE cards SET isRegistered = 1 WHERE CID = '{}'".format(CID))
        conn.commit()
        conn.close()

    def createTerminal(self, address):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        generatedUUID = uuid.uuid1()
        c.execute("INSERT INTO terminals VALUES ('{}', '{}', '0')".format(generatedUUID, address))
        conn.commit()
        conn.close()
        return Terminal(generatedUUID, address)

    def createTerminalWithTID(self, address, TID):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
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
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("SELECT * FROM employees")
        emps = c.fetchall()
        conn.close()
        return emps

    def getAllBindings(self):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("SELECT CID FROM cards WHERE EID IS NOT NULL")
        binds = c.fetchall()
        conn.close()
        return binds

    def getAllCards(self):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("SELECT * FROM cards")
        cards = c.fetchall()
        conn.close()
        return cards

    def getAllTerminals(self):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("SELECT * FROM terminals")
        terms = c.fetchall()
        conn.close()
        return terms

    def getLogs(self):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("SELECT * FROM logs")
        logs = c.fetchall()
        conn.close()
        return logs

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
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("DELETE FROM employees WHERE EID = '{}'".format(EID))
        conn.close()

    def deleteCard(self, CID):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("DELETE FROM cards WHERE CID = '{}'".format(CID))
        conn.close()

    def getEmployeeById(self, EID):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
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

    def getTerminalById(self, TID):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("SELECT * FROM terminals WHERE TID='{}'".format(TID))
        terminal = self.c.fetchone()
        if terminal is None:
            print("There is no such terminal")
            conn.close()
            return None
        conn.close()
        return Terminal(terminal[0], terminal[1])

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
            tmp = self.createTerminal("rav")

        server.registerTerminal(tmp.TID)

        server.loadTerminals()
        server.loadCards()
