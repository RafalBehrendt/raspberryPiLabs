import Constants
from Employee import Employee
import sqlite3
import datetime

class Server:
    address = "192.168.0.2"
    ID = "1"
    conn = sqlite3.connect('../database/company.db')
    c = conn.cursor()
    listOfTerminals = []
    checkedInEmployees = []

    def retrieveData(self, TID, CID):
        #if self.listOfTerminals.__contains__(TID):
            print(TID, CID)
            self.c.execute("SELECT * FROM cards WHERE CID='{}'".format(CID))
            cardQuery = self.c.fetchone()
            if cardQuery is not None:
                self.c.execute("SELECT EID FROM bindings WHERE CID='{}'".format(CID))
                employee = self.c.fetchone()[0]
                if employee is not None:
                    if self.checkedInEmployees.__contains__(employee):
                        print("Checking employee {} out".format(employee))
                        self.checkOut(TID, CID, employee)
                    else:
                        print("Checking employee {} in".format(employee))
                        self.checkIn(CID, TID, employee)
                        self.checkedInEmployees.append(employee)
                else:
                    print(Constants.CARD_NOT_BINDED)
                    self.logUnbindedCardScan()
            else:
                print("Registering new card")
                self.registerUnknownCard()
       # else:
        #    print(Constants.TERMINAL_NOT_REGISTERED)

    def loadTerminals(self):
        self.c.execute("SELECT TID FROM terminals")
        self.listOfTerminals = self.c.fetchall()
        print("Loaded terminals")

    def registerTerminal(self, TID, address):
        self.c.execute("INSERT INTO terminals VALUES ('{}', '{}')".format(TID, address))
        self.conn.commit()

    def unregisterTerminal(self, TID):
        self.c.execute("DELETE FROM terminals WHERE TID='{}'".format(TID))
        self.conn.commit()

    def getEmployeeById(self, EID):
        self.c.execute("SELECT * FROM employees WHERE ID='{}'".format(EID))
        self.conn.commit()

    def checkIn(self, CID, TID, EID):
        self.c.execute("INSERT INTO logs VALUES ('{}', '{}', '{}', '{}', '{}')"
                        .format(CID, TID, EID, Constants.Action.checkIn, datetime.datetime.now()))
        self.conn.commit()

    def checkOut(self, TID, CID, EID):
        self.c.execute("INSERT INTO logs VALUES ('{}', '{}', '{}', '{}', '{}')"
                        .format(CID, TID, EID, Constants.Action.checkOut, datetime.datetime.now()))
        self.conn.commit()

    def registerUnknownCard(self, CID, TID):
        self.c.execute("INSERT INTO logs VALUES ('{}', '{}', '{}', '{}')"
                       .format(CID, TID, None, Constants.Action.unknown, datetime.datetime.now()))
        self.conn.commit()

    def logUnbindedCardScan(self, CID):
        self.c.execute("INSERT INTO logs VALUES ('{}', '{}', '{}', '{}', '{}')"
                       .format(CID, None, None, Constants.Action.unbinded, datetime.datetime.now()))
        self.conn.commit()

    def bindCardToEmployee(self, CID, EID):
        self.c.execute("INSERT INTO bindings VALUES ('{}', '{}')".format(EID, CID))
        self.conn.commit()


