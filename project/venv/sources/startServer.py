from init import init, server
from serverGuiManager import serverGuiManager
from getpass import getpass

def runServer():

    login = input("Login: ")
    password = getpass()

    gui = serverGuiManager()
    server.connectToBroker(login, password)
    server.setGui(gui)
    gui.createMainWindow()
    gui.window.mainloop()

    server.disconnectFromBroker()


if __name__ == "__main__":

    init()
    runServer()
