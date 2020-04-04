import tkinter
from init import listOfCards, ms

class TerminalGuiManager:

    introLabel = None
    cardLabel = None

    def __init__(self, terminal):
        self.terminal = terminal
        self.window = tkinter.Tk()

    def createMainWindow(self):
        self.window.geometry("300x200")
        self.window.title("TERMINAL")
        self.introLabel = tkinter.Label(self.window, text="Terminal ID: {}".format(self.terminal.TID))
        self.introLabel.grid(row=0, columnspan=5)

        self.cardLabel = tkinter.Label(self.window, text="Current Card: {}".format(self.terminal.menu.shc()))
        self.cardLabel.grid(row=2, columnspan=5)

        cardButtons = []

        for i in range(len(listOfCards)):
            cardButtons.append(tkinter.Button(self.window, text="Card {}".format(i),
                                command=lambda bounded_i=i: self.changeCard(bounded_i)))
            cardButtons[i].grid(row=3+int(i/3), column=i%3)

        scanButton = tkinter.Button(self.window, text="Scan current card",
                                    command=lambda:  self.terminal.scanCardMQTT(self.terminal.menu.currentCard))
        scanButton.grid(row = 999, column = 0)

    def changeCard(self, card):
        self.terminal.menu.chc(card)
        self.cardLabel.config(text="Current Card: {}".format(self.terminal.menu.shc()))