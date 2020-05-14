import sys
from getpass import getpass

import Constants
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


def initiationUnsuccessful():
    print("""Provide number to choose from available terminals, or provide string
                  to open unknown terminal""")
    print("Available terminals: ")
    i = 0
    for _ in listOfTerminals:
        print("{}. {}".format(i, listOfTerminals[i].toString()))
        i += 1


if __name__ == "__main__":

    init()

    if len(sys.argv) == 2:
        if sys.argv[1].isdigit():
            if int(sys.argv[1]) < len(listOfTerminals):
                runClient(listOfTerminals[int(sys.argv[1])])
            else:
                initiationUnsuccessful()
        else:
            terminal = Terminal(sys.argv[1], Constants.HOSTNAME)
            runClient(terminal)
    else:
        initiationUnsuccessful()
