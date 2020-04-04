#!/usr/bin/env python3

import Constants
import sqlite3
import datetime
import csv
from ManagementService import ManagementService
import paho.mqtt.client as mqtt
import tkinter
from menu import Menu

class Server:
    broker = "localhost"
    conn = sqlite3.connect('../database/company.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()
    listOfTerminals = []
    listOfCards = []
    checkedInEmployees = []

    client = mqtt.Client()
    menu = Menu()

    def __init__(self):
        self.loadTerminals()
        self.loadCards()

    def receiveData(self, TID, CID):
        print("Received card {} from terminal {}".format(CID, TID))
        if self.listOfTerminals.__contains__(TID):
            self.c.execute("SELECT * FROM cards WHERE CID='{}' AND isRegistered = 1".format(CID))
            cardQuery = self.c.fetchone()
            if cardQuery is not None:
                self.c.execute("SELECT EID FROM cards WHERE CID='{}'".format(CID))
                employee = self.c.fetchone()
                if employee[0] != "None":
                    if self.checkedInEmployees.__contains__(employee[0]):
                        print("Checking employee {} out".format(employee[0]))
                        self.checkOut(TID, CID, employee[0])
                    else:
                        print("Checking employee {} in".format(employee[0]))
                        self.checkIn(CID, TID, employee[0])
                        self.checkedInEmployees.append(employee[0])
                else:
                    print(Constants.CARD_NOT_BINDED)
                    self.logUnbindedCardScan(CID, TID)
            else:
                print("Registering new card")
                self.registerUnknownCard(CID, TID)
        else:
            print(Constants.TERMINAL_NOT_REGISTERED)

    def loadTerminals(self):
        self.listOfTerminals.clear()
        self.c.execute("SELECT TID FROM terminals WHERE isRegistered = '1'")
        lot = self.c.fetchall()
        for terminal in lot:
            self.listOfTerminals.append(terminal[0])
        print("Loaded terminals")

    def loadCards(self):
        self.listOfCards.clear()
        self.c.execute("SELECT CID FROM cards WHERE isRegistered = 1")
        cards = self.c.fetchall()
        for card in cards:
            self.listOfCards.append(card[0])
        print("Loaded cards")

    def registerTerminal(self, TID):
        self.c.execute("UPDATE terminals SET isRegistered = '1' WHERE TID = '{}'".format(TID))
        self.conn.commit()
        self.loadTerminals()

    def unregisterTerminal(self, TID):
        self.c.execute("UPDATE terminals SET isRegistered = '0' WHERE TID = '{}'".format(TID))
        self.conn.commit()
        self.loadTerminals()

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
        self.checkedInEmployees.remove(EID)

    def registerUnknownCard(self, CID, TID):
        self.c.execute("UPDATE cards SET isRegistered = '1' WHERE CID = '{}'".format(CID))
        self.conn.commit()
        self.c.execute("INSERT INTO logs VALUES ('{}', '{}', '{}', '{}', '{}')"
                       .format(CID, TID, None, Constants.Action.unknown, datetime.datetime.now()))
        self.conn.commit()
        self.loadCards()

    def logUnbindedCardScan(self, CID, TID):
        self.c.execute("INSERT INTO logs VALUES ('{}', '{}', '{}', '{}', '{}')"
                       .format(CID, TID, None, Constants.Action.unbinded, datetime.datetime.now()))
        self.conn.commit()

    def bindCardToEmployee(self, CID, EID):
        self.c.execute("SELECT EID FROM cards WHERE CID='{}'".format(CID))
        query = self.c.fetchone()
        if query[0] == "None":
            self.c.execute("UPDATE cards SET EID ='{}' WHERE CID ='{}'".format(EID, CID))
            self.conn.commit()
            print("Binded card {} to employee {}".format(CID, EID))
        else:
            print("Card already binded")

    def unbindCardFromEmployee(self, CID):
        self.c.execute("SELECT EID FROM cards WHERE CID='{}'".format(CID))
        query = self.c.fetchone()
        if query[0] != "None":
            self.c.execute("UPDATE cards SET EID='{}' WHERE CID='{}'".format(None, CID))
            self.conn.commit()
            print("Card unbinded")
        else:
            print("Card {} is not binded".format(CID))

    def generateReport(self, EID):
        self.c.execute("SELECT datetime FROM logs WHERE EID='{}' AND action='{}'".format(EID, Constants.Action.checkIn))
        employeeCheckIn = self.c.fetchall()
        self.c.execute("SELECT datetime FROM logs WHERE EID='{}' AND action='{}'".format(EID, Constants.Action.checkOut)) #make one query maybe?
        employeeCheckOut = self.c.fetchall()
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

    def convertSecondsToTime(self, totalSeconds):
        hours = divmod(totalSeconds, 3600)
        minutes = divmod(hours[1], 60)
        seconds = divmod(minutes[1], 1)
        return(hours[0], minutes[0], seconds[0])

    def processMessage(self, client, userdata, message):
        decodedMessage = (str(message.payload.decode("utf-8"))).split(".")

        if decodedMessage[0] != Constants.CLIENT_CONN and decodedMessage[0] != Constants.CLIENT_DISCONN:
            self.receiveData(decodedMessage[0], decodedMessage[1])
        else:
            print(decodedMessage[0] + " : " + decodedMessage[1])

    def connectToBroker(self):
        self.client.connect(self.broker)
        self.client.on_message = self.processMessage
        self.client.loop_start()
        self.client.subscribe("CID/TID")

    def disconnectFromBroker(self):
        self.client.loop_stop()
        self.client.disconnect()














