#!/usr/bin/env python3

import Constants
import sqlite3
import datetime
import csv
from ManagementService import ManagementService
import paho.mqtt.client as mqtt
import pdb
#from serverGuiManager import serverGuiManager

class Server:
    broker = "localhost"
    listOfTerminals = []
    listOfCards = []
    checkedInEmployees = []

    client = mqtt.Client()

    def __init__(self):
        self.loadTerminals()
        self.loadCards()
        self.loadCheckedInEmployees()

    def receiveData(self, TID, CID):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        print("Received card {} from terminal {}".format(CID, TID))
        if self.listOfTerminals.__contains__(TID):
            c.execute("SELECT * FROM cards WHERE CID='{}' AND isRegistered = 1".format(CID))
            cardQuery = c.fetchone()
            if cardQuery is not None:
                c.execute("SELECT EID FROM cards WHERE CID='{}'".format(CID))
                employee = c.fetchone()
                if employee[0] != "None":
                    if self.checkedInEmployees.__contains__(employee[0]):
                        retVal="Checking employee {} out".format(employee[0])
                        print(retVal)
                        self.checkOut(TID, CID, employee[0])
                        return retVal
                    else:
                        retVal="Checking employee {} in".format(employee[0])
                        print(retVal)
                        self.checkIn(CID, TID, employee[0])
                        return retVal
                else:
                    retVal = "Scanned unbound card {}".format(CID)
                    print(retVal)
                    self.logUnboundCardScan(CID, TID)
                    return retVal
            else:
                retVal="Registering new card {}".format(CID)
                print(retVal)
                self.registerUnknownCard(CID, TID)
                return retVal
        else:
            print(Constants.TERMINAL_NOT_REGISTERED)
            return Constants.TERMINAL_NOT_REGISTERED


    def loadTerminals(self):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        self.listOfTerminals.clear()
        c.execute("SELECT TID FROM terminals WHERE isRegistered = '1'")
        lot = c.fetchall()
        for terminal in lot:
            self.listOfTerminals.append(terminal[0])
        print("Loaded terminals")
        conn.close()

    def loadCards(self):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        self.listOfCards.clear()
        c.execute("SELECT CID FROM cards WHERE isRegistered = 1")
        cards = c.fetchall()
        for card in cards:
            self.listOfCards.append(card[0])
        print("Loaded cards")
        conn.close()

    def loadCheckedInEmployees(self):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        self

    def registerTerminal(self, TID):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("UPDATE terminals SET isRegistered = '1' WHERE TID = '{}'".format(TID))
        conn.commit()
        self.loadTerminals()
        conn.close()


    def unregisterTerminal(self, TID):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("UPDATE terminals SET isRegistered = '0' WHERE TID = '{}'".format(TID))
        conn.commit()
        self.loadTerminals()
        conn.close()

    def getEmployeeById(self, EID):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("SELECT * FROM employees WHERE ID='{}'".format(EID))
        conn.commit()
        conn.close()

    def checkIn(self, CID, TID, EID):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("INSERT INTO logs VALUES ('{}', '{}', '{}', '{}', '{}')"
                        .format(CID, TID, EID, Constants.Action.checkIn, datetime.datetime.now()))
        self.checkedInEmployees.append(EID)
        conn.commit()
        conn.close()

    def checkOut(self, TID, CID, EID):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("INSERT INTO logs VALUES ('{}', '{}', '{}', '{}', '{}')"
                        .format(CID, TID, EID, Constants.Action.checkOut, datetime.datetime.now()))
        conn.commit()
        self.checkedInEmployees.remove(EID)
        conn.close()

    def registerUnknownCard(self, CID, TID):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("UPDATE cards SET isRegistered = '1' WHERE CID = '{}'".format(CID))
        conn.commit()
        c.execute("INSERT INTO logs VALUES ('{}', '{}', '{}', '{}', '{}')"
                       .format(CID, TID, None, Constants.Action.unknown, datetime.datetime.now()))
        conn.commit()
        self.loadCards()

    def logUnboundCardScan(self, CID, TID):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("INSERT INTO logs VALUES ('{}', '{}', '{}', '{}', '{}')"
                  .format(CID, TID, None, Constants.Action.unbound, datetime.datetime.now()))
        conn.commit()
        conn.close()

    def bindCardToEmployee(self, CID, EID):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("SELECT EID FROM cards WHERE CID='{}'".format(CID))
        query = c.fetchone()
        if query[0] == "None":
            c.execute("UPDATE cards SET EID ='{}' WHERE CID ='{}'".format(EID, CID))
            conn.commit()
            print("Bound card {} to employee {}".format(CID, EID))
            conn.close()
            return True
        else:
            print("Card already bound")
            conn.close()
            return False

    def unbindCardFromEmployee(self, CID):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("SELECT EID FROM cards WHERE CID='{}'".format(CID))
        query = c.fetchone()
        if query[0] != "None":
            c.execute("UPDATE cards SET EID='{}' WHERE CID='{}'".format(None, CID))
            conn.commit()
            conn.close()
            retVal = "Card {} unbound".format(CID)
            print(retVal)
            return retVal
        else:
            conn.close()
            retVal = "Card {} is not bound".format(CID)
            print(retVal)
            return retVal

    def generateReport(self, EID):
        conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute("SELECT datetime FROM logs WHERE EID='{}' AND action='{}'".format(EID, Constants.Action.checkIn))
        employeeCheckIn = c.fetchall()
        c.execute("SELECT datetime FROM logs WHERE EID='{}' AND action='{}'".format(EID, Constants.Action.checkOut))
        employeeCheckOut = c.fetchall()
        employee = ManagementService.getEmployeeById(ManagementService, EID)
        print(employee.toString())
        with open('../reports/{}.csv'.format(EID), 'w', newline='') as csvflie:
            writer = csv.writer(csvflie)
            writer.writerow([employee.ID, employee.name, employee.surname])
            writer.writerow([])
            writer.writerow(["Time of checking in", "Time of checking out", "Total hours", "Total minutes", "Total seconds"])
            totalTime=0
            for (checkIn, checkOut) in zip(employeeCheckIn, employeeCheckOut):
                diffrence = checkOut[0] - checkIn[0]
                durInSec = diffrence.total_seconds()
                time = self.convertSecondsToTime(durInSec)
                writer.writerow([checkIn[0], checkOut[0], int(time[0]), int(time[1]), int(time[2])])
                totalTime += durInSec
            if len(employeeCheckIn) > len(employeeCheckOut):
                lastCheckInLog = employeeCheckIn[-1]
                diffrence = datetime.datetime.now() - lastCheckInLog[0]
                durInSec = diffrence.total_seconds()
                time = self.convertSecondsToTime(durInSec)
                writer.writerow([lastCheckInLog[0], "Still in work", int(time[0]), int(time[1]), int(time[2])])
                totalTime += durInSec
            time = self.convertSecondsToTime(totalTime)
            writer.writerow([])
            writer.writerow(["","Hours","Minutes","Seconds"])
            writer.writerow(["Total time of work:", int(time[0]), int(time[1]), int(time[2])])
        print("Created report {} in reports folder".format(EID))
        conn.close()

    def convertSecondsToTime(self, totalSeconds):
        hours = divmod(totalSeconds, 3600)
        minutes = divmod(hours[1], 60)
        seconds = divmod(minutes[1], 1)
        return(hours[0], minutes[0], seconds[0])


    def disconnectFromBroker(self):
        self.client.loop_stop()
        self.client.disconnect()
