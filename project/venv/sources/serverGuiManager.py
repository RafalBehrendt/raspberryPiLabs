import tkinter
from init import listOfTerminals, listOfCards, ms, reloadTerminals, server
import Constants
import sqlite3
import pdb

class serverGuiManager:
    introLabel = None
    terminalsStatus = []
    terminalsLabels = []
    statusLabels = []

    messageLabel = None
    cardList = None
    employeeList = None
    existingTerminalsList = None

    def __init__(self):
        self.window = tkinter.Tk()
        self.registeredTerminalsList = tkinter.Spinbox(self.window)

        server.client.connect(server.broker)
        server.client.on_message = self.processMessage
        server.client.loop_start()
        server.client.subscribe("CID/TID")

    def createMainWindow(self):
        self.window.geometry("300x200")
        self.window.title("SERVER")
        self.introLabel = tkinter.Label(self.window, text="Server listening to MQTT")
        self.introLabel.grid(row=0, column=0)

        for terminal in server.listOfTerminals:
            self.writeDownNewTerminal(terminal)

        addNewTerminalLabel = tkinter.Label(self.window, text="Register new terminal: ")
        addNewTerminalEntry = tkinter.Entry(self.window, width=10)
        addNewTerminalButton = tkinter.Button(self.window, text="Register",
                                              command=lambda: self.registerNewTerminal(addNewTerminalEntry.get()))
        addNewTerminalLabel.grid(row=1, column=2)
        addNewTerminalEntry.grid(row=1, column=3)
        addNewTerminalButton.grid(row=1, column=4)

        registerExistingTerminalLabel = tkinter.Label(self.window, text="Register existing terminal: ")
        self.existingTerminalsList = tkinter.Spinbox(self.window, values=list(map(lambda x: x.TID, listOfTerminals)))
        registerExistingTerminalButton = tkinter.Button(self.window, text="Register",
                                                        command=lambda: self.registerExistingTerminal(
                                                            self.existingTerminalsList.get()))
        registerExistingTerminalLabel.grid(row=2, column=2)
        self.existingTerminalsList.grid(row=2, column=3)
        registerExistingTerminalButton.grid(row=2, column=4)

        unregisterExistingTerminalLabel = tkinter.Label(self.window, text="Unegister terminal: ")
        self.registeredTerminalsList = tkinter.Spinbox(self.window, values=server.listOfTerminals)
        unregisterExistingTerminalButton = tkinter.Button(self.window, text="Unregister",
                                                          command=lambda: self.unregisterTerminal(self.registeredTerminalsList.get()))
        unregisterExistingTerminalLabel.grid(row=3, column=2)
        self.registeredTerminalsList.grid(row=3, column=3)
        unregisterExistingTerminalButton.grid(row=3, column=4)

        bindCardLabel = []
        bindCardLabel.append(tkinter.Label(self.window, text="Bind card to employee"))
        bindCardLabel.append(tkinter.Label(self.window, text="Card ID"))
        bindCardLabel.append(tkinter.Label(self.window, text="Employee Name"))
        bindCardLabel[0].grid(row=4, column=2)
        bindCardLabel[1].grid(row=4, column=3)
        bindCardLabel[2].grid(row=4, column=4)


        self.cardList = tkinter.Spinbox(self.window, values=listOfCards)
        self.employeeList = tkinter.Spinbox(self.window, values=list(map(lambda x: x[0], ms.getAllEmployees())))
        bindButton = tkinter.Button(self.window, text="Bind",
                                    command=lambda: self.bindCardToEmployee(self.cardList.get(), self.employeeList.get()))

        bindButton.grid(row=5, column=2)
        self.cardList.grid(row=5, column=3)
        self.employeeList.grid(row=5, column=4)

        generateReportLabel = tkinter.Label(self.window, text="Generate report:")
        generateReportButton = tkinter.Button(self.window, text="Generate",
                                              command=lambda: self.generateReport(self.employeeList.get()))
        generateReportLabel.grid(row=6, column=2)
        generateReportButton.grid(row=6, column=3)

        self.messageLabel = tkinter.Label(self.window, text="Hello")
        self.messageLabel.grid(row=7, column=2, columnspan=3, pady=5)

    def registerNewTerminal(self, newTID):
        if newTID == "":
            self.log("Provide non empty TID", "yellow")

        if not ms.createTerminalWithTID("localhost", newTID):
            self.log("TID not unique. Provide unique ID for terminal", "red")
            return
        server.registerTerminal(newTID)
        self.writeDownNewTerminal(newTID)
        reloadTerminals()
        self.existingTerminalsList.config(value=list(map(lambda x: x.TID, listOfTerminals)))
        self.registeredTerminalsList.config(value=server.listOfTerminals)
        self.log("New terminal {} registered".format(newTID), "green")

    def registerExistingTerminal(self, TID):
        if server.listOfTerminals.__contains__(TID):
            self.log("Terminal already registered", "red")
        else:
            server.registerTerminal(TID)
            self.registeredTerminalsList.config(value=server.listOfTerminals)
            self.writeDownNewTerminal(TID)
            self.log("Terminal registered", "green")


    def unregisterTerminal(self, TID):
        server.unregisterTerminal(TID)
        self.log("Unregistered terminal", "green")
        i = 0
        for terminal in self.terminalsLabels:
            if terminal.cget("text") == TID:
                self.statusLabels[i].destroy()
                self.statusLabels.remove(self.statusLabels[i])
                self.terminalsLabels.remove(terminal)
                terminal.destroy()
            i += 1
        self.refreshTerminals()
        self.registeredTerminalsList.config(values=server.listOfTerminals)

    def bindCardToEmployee(self, CID, EID):
        if server.bindCardToEmployee(CID, EID):
            self.log("Bound card {} to employee {}".format(CID, EID), "green")
        else:
            self.log("Card already binded to some employee", "yellow")

    def generateReport(self, EID):
        server.generateReport(EID)
        self.log("Generated report for employee {}".format(EID), "green")

    def writeDownNewTerminal(self, terminal):
        self.terminalsStatus.append("OFFLINE")
        self.terminalsLabels.append(tkinter.Label(self.window, text=terminal))
        self.statusLabels.append(tkinter.Label(self.window, text=self.terminalsStatus[-1], fg="red"))
        self.terminalsLabels[-1].grid(row=len(self.terminalsLabels), column=0)
        self.statusLabels[-1].grid(row=len(self.terminalsLabels), column=1)

    def refreshTerminals(self):
        i = 0
        for terminal in self.terminalsLabels:
            print(terminal)
            terminal.grid(row=i+1, column=0)
            self.statusLabels[i].grid(row=i+1, column=1)
            i+=1

    def log(self, message, color):
        self.messageLabel.config(text=message, fg=color)

    def processMessage(self, client, userdata, message):
        decodedMessage = (str(message.payload.decode("utf-8"))).split(".")

        if decodedMessage[0] == Constants.CLIENT_CONN:
            print(decodedMessage[0] + " : " + decodedMessage[1])
            self.log("Connected!", "green")
        elif decodedMessage[0] == Constants.CLIENT_DISCONN:
            self.log("Disconnected!", "red")
            print(decodedMessage[0] + " : " + decodedMessage[1])
        else:
            returnedVal=server.receiveData(decodedMessage[1], decodedMessage[0])
            print(returnedVal)
            self.log(returnedVal, "yellow")
            print("executed3!")

