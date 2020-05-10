import sys
from getpass import getpass

from init import init, listOfTerminals
from terminalGuiManager import TerminalGuiManager
from Terminal import Terminal


def runClient(terminal):

    login = input("Login: ")
    password = getpass()

    gui = TerminalGuiManager(terminal)
    terminal.setGui(gui)
    terminal.connectToBroker(login, password)
    gui.createMainWindow()
    gui.window.mainloop()
    terminal.disconnectFromBroker()


if __name__ == "__main__":

    init()

    if len(sys.argv) == 2:
        if sys.argv[1].isdigit():
            runClient(listOfTerminals[int(sys.argv[1])])
        else:
            terminal = Terminal(sys.argv[1], "rav")
            runClient(terminal)
    else:
        print("""Provide number to choose from available terminals, or provide string
              to open unknown terminal""")
        print("Available terminals: ")
        i = 0
        for terminal in listOfTerminals:
            print("{}. {}".format(i, listOfTerminals[i].toString()))
            i += 1
