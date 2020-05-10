import tkinter
from tkinter import simpledialog

from init import listOfTerminals, listOfCards, ms, reloadTerminals, server


class serverGuiManager:
    introLabel = None
    terminalsStatus = []
    terminalsLabels = []
    statusLabels = []
    terminalDisconnectButtons = []

    messageLabel = None
    cardList = None
    employeeList = None
    existingTerminalsList = None

    def __init__(self):
        self.window = tkinter.Tk()
        self.registeredTerminalsList = tkinter.Spinbox(self.window)

    def createMainWindow(self):
        # self.window.geometry("1000x300")
        self.window.title("SERVER")
        self.introLabel = tkinter.Label(self.window, text="Server listening to MQTT")
        self.introLabel.grid(row=0, column=0)

        for terminal in server.listOfTerminals:
            self.writeDownNewTerminal(terminal)

        addNewTerminalLabel = tkinter.Label(self.window, text="Register new terminal: ")
        addNewTerminalEntry = tkinter.Entry(self.window, width=10)
        addNewTerminalButton = tkinter.Button(self.window, text="Register",
                                              command=lambda: self.registerNewTerminal(addNewTerminalEntry.get()))
        addNewTerminalLabel.grid(row=1, column=3)
        addNewTerminalEntry.grid(row=1, column=4)
        addNewTerminalButton.grid(row=1, column=5)

        registerExistingTerminalLabel = tkinter.Label(self.window, text="Register existing terminal: ")
        self.existingTerminalsList = tkinter.Spinbox(self.window, values=list(map(lambda x: x.TID, listOfTerminals)))
        registerExistingTerminalButton = tkinter.Button(self.window, text="Register",
                                                        command=lambda: self.registerExistingTerminal(
                                                            self.existingTerminalsList.get()))
        registerExistingTerminalLabel.grid(row=2, column=3)
        self.existingTerminalsList.grid(row=2, column=4)
        registerExistingTerminalButton.grid(row=2, column=5)

        unregisterExistingTerminalLabel = tkinter.Label(self.window, text="Unegister terminal: ")
        self.registeredTerminalsList = tkinter.Spinbox(self.window, values=server.listOfTerminals)
        unregisterExistingTerminalButton = tkinter.Button(self.window, text="Unregister",
                                                          command=lambda: self.unregisterTerminal(
                                                              self.registeredTerminalsList.get()))
        unregisterExistingTerminalLabel.grid(row=3, column=3)
        self.registeredTerminalsList.grid(row=3, column=4)
        unregisterExistingTerminalButton.grid(row=3, column=5)

        bindCardLabel = []
        bindCardLabel.append(tkinter.Label(self.window, text="Bind card to employee"))
        bindCardLabel.append(tkinter.Label(self.window, text="Card ID"))
        bindCardLabel.append(tkinter.Label(self.window, text="Employee Name"))
        bindCardLabel[0].grid(row=4, column=3)
        bindCardLabel[1].grid(row=4, column=4)
        bindCardLabel[2].grid(row=4, column=5)

        self.cardList = tkinter.Spinbox(self.window, values=listOfCards)
        self.employeeList = tkinter.Spinbox(self.window, values=list(map(lambda x: x[0], ms.getAllEmployees())))
        bindButton = tkinter.Button(self.window, text="Bind",
                                    command=lambda: self.bindCardToEmployee(self.cardList.get(),
                                                                            self.employeeList.get()))

        bindButton.grid(row=5, column=3)
        self.cardList.grid(row=5, column=4)
        self.employeeList.grid(row=5, column=5)

        unbindButton = tkinter.Button(self.window, text="Unbind",
                                      command=lambda: self.unbindCard(self.cardList.get()))

        unbindButton.grid(row=6, column=3)

        generateReportLabel = tkinter.Label(self.window, text="Generate report:")
        generateReportButton = tkinter.Button(self.window, text="Generate",
                                              command=lambda: self.generateReport(self.employeeList.get()))
        generateReportLabel.grid(row=7, column=3)
        generateReportButton.grid(row=7, column=4)

        showLogsButton = tkinter.Button(self.window, text="Show logs",
                                        command=lambda: self.showLogs())
        showLogsButton.grid(row=8, column=3, columnspan=2)

        self.messageLabel = tkinter.Label(self.window, text="Hello")
        self.messageLabel.grid(row=9, column=3, columnspan=999, pady=5)

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

    def unbindCard(self, CID):
        self.log(server.unbindCardFromEmployee(CID), "green")

    def generateReport(self, EID):
        server.generateReport(EID)
        self.log("Generated report for employee {}".format(EID), "green")

    def showLogs(self):
        logEntries = ms.getLogs()
        cells = []
        printLogWindow = tkinter.Tk()

        logHeaders = []

        logHeaders.append(tkinter.Label(printLogWindow, text="CardID"))
        logHeaders.append(tkinter.Label(printLogWindow, text="TerminalID"))
        logHeaders.append(tkinter.Label(printLogWindow, text="EmployeeID"))
        logHeaders.append(tkinter.Label(printLogWindow, text="Action"))
        logHeaders.append(tkinter.Label(printLogWindow, text="Date"))

        i = 0
        for logHeader in logHeaders:
            logHeader.grid(row=0, column=i)
            i += 1

        i = 1
        for log in logEntries:
            j = 0
            for cell in log:
                cells.append(tkinter.Label(printLogWindow, text=cell))
                cells[-1].grid(row=i, column=j)
                j += 1
            i += 1

    def writeDownNewTerminal(self, terminal):
        self.terminalsStatus.append("OFFLINE")
        self.terminalsLabels.append(tkinter.Label(self.window, text=terminal))
        self.statusLabels.append(tkinter.Label(self.window, text=self.terminalsStatus[-1], fg="red"))
        self.terminalDisconnectButtons.append(tkinter.Button(self.window, text="Disconnect",
                                                             command=lambda: self.disconnectTerminal(terminal)))
        self.terminalsLabels[-1].grid(row=len(self.terminalsLabels), column=0)
        self.statusLabels[-1].grid(row=len(self.terminalsLabels), column=1)
        self.terminalDisconnectButtons[-1].grid(row=len(self.terminalsLabels), column=2)

    def refreshTerminals(self):
        i = 0
        for terminal in self.terminalsLabels:
            print(terminal)
            terminal.grid(row=i + 1, column=0)
            self.statusLabels[i].grid(row=i + 1, column=1)
            i += 1

    def log(self, message, color):
        self.messageLabel.config(text=message, fg=color)

    def disconnectTerminal(self, terminal):
        message = simpledialog.askstring("Provide message", "Provide reason for disconnection")
        server.disconnectTerminal(terminal, message)

    def setTerminalOnline(self, TID):
        i = 0
        for terminal in self.terminalsLabels:
            if terminal.cget("text") == TID:
                self.statusLabels[i].config(text="ONLINE", fg="green")
            i += 1

    def setTerminalOffline(self, TID):
        i = 0
        for terminal in self.terminalsLabels:
            if terminal.cget("text") == TID:
                self.statusLabels[i].config(text="OFFLINE", fg="red")
            i += 1
