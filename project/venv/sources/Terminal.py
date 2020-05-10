from tkinter import messagebox

import paho.mqtt.client as mqtt
import Constants

class Terminal:

    def __init__(self, TID, broker):
        self.TID = TID
        self.broker = broker  # rav
        self.port = 8883

        self.client = mqtt.Client()

    def setGui(self, gui):
        self.terminalGui = gui

    def sendData(self, CID, server):
        server.receiveData(self.TID, CID)

    def scanCard(self, CID):
        from init import server
        print("Scanned card: {}".format(CID))
        self.sendData(CID, server)

    def toString(self):
        return "TID: {} \naddress: {}".format(self.TID, self.broker)

    def scanCardMQTT(self, msg):
        print("msg: {} | TID: {}".format(msg, self.TID))
        self.client.publish("CID/TID", msg + "." + self.TID)

    def processMessage(self, client, userdata, message):
        decodedMessage = (str(message.payload.decode("utf-8"))).split(".")
        if decodedMessage[0] == self.TID:
            messagebox.showinfo("Message from server", "You have been disconnected by server. Reason : {}".format(decodedMessage[1]))
            self.terminalGui.quit()
            self.client.disconnect()
            exit(0)

    def connectToBroker(self, login, password):
        self.client.tls_set(Constants.CERT_PATH)
        self.client.username_pw_set(username=login, password=password)
        self.client.connect(self.broker, self.port)
        self.client.on_message = self.processMessage
        self.client.loop_start()
        self.client.subscribe("server/name")
        self.scanCardMQTT(Constants.CLIENT_CONN)

    def disconnectFromBroker(self):
        self.scanCardMQTT(Constants.CLIENT_DISCONN)
        self.client.disconnect()
