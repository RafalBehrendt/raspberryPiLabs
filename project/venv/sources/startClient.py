import sys
from init import init, listOfTerminals
from terminalGuiManager import TerminalGuiManager
import psutil
from Terminal import Terminal

def runClient(terminal):

    gui = TerminalGuiManager(terminal)
    terminal.connectToBroker()
    gui.createMainWindow()

    # for proc in psutil.process_iter():
    #     try:
    #         files = proc.open_files()
    #         if files:
    #             for _file in files:
    #                 if _file.path == "../database/company.db":
    #                     print("still connected!")
    #     except psutil.NoSuchProcess as err:
    #         print(err)
    #     print("Not connected!")


    gui.window.mainloop()
    terminal.disconnectFromBroker()

if __name__ == "__main__":

    init()

    print(len(sys.argv))

    if len(sys.argv) == 2:
        if sys.argv[1].isdigit():
           runClient(listOfTerminals[int(sys.argv[1])])
        else:
            terminal = Terminal(sys.argv[1], "localhost")
            runClient(terminal)
    else:
        print("""Provide number to choose from available terminals, or provide string
              to open unknown terminal""")
        print("Available terminals: ")
        i=0
        for terminal in listOfTerminals:
            print("{}. {}".format(i, listOfTerminals[i].toString()))
            i+=1



