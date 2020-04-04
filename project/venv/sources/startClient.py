from init import listOfTerminals, init
import sys
from terminalGuiManager import TerminalGuiManager

def runClient(terminal):

    terminal.menu.init()
    gui = TerminalGuiManager(terminal)
    terminal.connectToBroker()
    gui.createMainWindow()
    gui.window.mainloop()

    terminal.disconnectFromBroker()

if __name__ == "__main__":

    init()

    if len(sys.argv) > 1:
        if int(sys.argv[1]) < 0 or int(sys.argv[1]) >= len(listOfTerminals):
            print("Provide correct terminal. Available terminals: ")
            i = 0
            for term in listOfTerminals:
                print("{}. {}".format(i, term.toString()))
                i += 1
        else:
            runClient(listOfTerminals[int(sys.argv[1])])

    else:
        print("Provide terminal")



