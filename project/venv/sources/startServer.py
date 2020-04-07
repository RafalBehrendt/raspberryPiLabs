from init import init, server
import sys
from serverGuiManager import serverGuiManager


def runServer():
    gui = serverGuiManager()
    gui.createMainWindow()
    gui.window.mainloop()

    server.disconnectFromBroker()


if __name__ == "__main__":
    init()
    runServer()
