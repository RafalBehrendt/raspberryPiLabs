import tkinter
from init import listOfTerminals


class serverGuiManager:

    introLabel = None

    def __init__(self, server):
        self.server = server
        self.window = tkinter.Tk()

    def createMainWindow(self):
        self.window.geometry("300x200")
        self.window.title("SERVER")
        self.introLabel = tkinter.Label(self.window, text="Server listening to MQTT")
        self.introLabel.grid(row=0, column=0)

        terminalsStatus = []
        terminalsLabels = []
        statusLabels = []
        i=0

        for terminal in listOfTerminals:
            terminalsStatus.append("OFFLINE")
            terminalsLabels.append(tkinter.Label(self.window, text="Terminal {}: ".format(terminal.TID)))
            statusLabels.append(tkinter.Label(self.window, text=terminalsStatus[i], fg="red"))
            terminalsLabels[i].grid(row=i+1, column=0)
            statusLabels[i].grid(row=i+1, column=1)
            i=i+1

        addNewTerminalLabel = tkinter.Label(self.window, text="Register new terminal: ")
        addNewTerminal = tkinter.Entry(self.window, width=10)
        addNewTerminalLabel.grid(row=1, column=2)
        addNewTerminal.grid(row = 1, column=3)

        registerNewTerminalLabel = tkinter.Label(self.window, text="Choose terminal to register: ")



        #scanButton = tkinter.Button(self.window, text="Scan current card",
         #                          command=lambda: self.terminal.scanCardMQTT(self.terminal.menu.currentCard))
        #scanButton.grid(row=999, column=0)
