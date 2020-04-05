import tkinter
from init import listOfCards

class TerminalGuiManager:

    introLabel = None
    cardLabel = None
    listOfCards = []

    def __init__(self, terminal):
        self.terminal = terminal
        self.window = tkinter.Tk()

    def createMainWindow(self):
        self.window.geometry("300x200")
        self.window.title("TERMINAL")
        self.introLabel = tkinter.Label(self.window, text="Terminal ID: {}".format(self.terminal.TID))
        self.introLabel.grid(row=0, columnspan=5)

        cardButtons = []

        i=0
        for card in listOfCards:
            cardButtons.append(tkinter.Button(self.window, text="Card {}".format(i),
                                command=lambda boundCard=card: self.scanCard(boundCard)))
            cardButtons[i].grid(row=3+int(i/3), column=i%3)
            i+=1

    def scanCard(self, card):
        self.terminal.scanCardMQTT(card)
        print("Scanned card: {}".format(card))


