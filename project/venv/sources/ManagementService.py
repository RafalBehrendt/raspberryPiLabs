import uuid
import sqlite3
from Employee import Employee


class ManagementService:
    conn = sqlite3.connect('../database/company.db')
    c = conn.cursor()

    def createEmployee(self, name, surname):
        self.c.execute("INSERT INTO employees VALUES ('{}', '{}', '{}')".format(uuid.uuid1(), name, surname))
        self.conn.commit()

    def createCard(self):
        self.c.execute("INSERT INTO cards VALUES ('{}')".format(uuid.uuid1()))
        self.conn.commit()

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

    def deleteEmployee(self, ID):
        self.c.execute("DELETE FROM employees WHERE ID = '{}'".format(ID))


