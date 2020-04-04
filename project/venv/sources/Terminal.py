#!/usr/bin/env python3

import paho.mqtt.client as mqtt
from menu import Menu
import Constants

class Terminal:

    def __init__(self, TID, broker):
        self.TID = TID
        self.broker = broker #localhost

        self.client = mqtt.Client()
        self.menu = Menu()

    def sendData(self, CID, server):
        server.receiveData(self.TID, CID)

    def scanCard(self, CID):
        from main import server
        print("Scanned card: {}".format(CID))
        self.sendData(CID, server)

    def toString(self):
        return "TID: {} \naddress: {}".format(self.TID, self.broker)

    def scanCardMQTT(self, msg):
        self.client.publish("CID/TID", msg + "." + self.TID)

    def connectToBroker(self):
        self.scanCardMQTT(Constants.CLIENT_CONN)
        self.client.connect(self.broker)

    def disconnectFromBroker(self):
        self.scanCardMQTT(Constants.CLIENT_DISCONN)
        self.client.disconnect()


