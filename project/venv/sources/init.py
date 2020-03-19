from Server import Server
from ManagementService import ManagementService
import DBManage

DBManage.initializeDB()
server = Server()
ms = ManagementService()
clientList = []
cardsList = []
employeeList = []


def dropDB():
    res = ""
    while res != "N" or res != "Y":
        res = input("You're about to drop whole database and create new one, proceed? [Y/N]: ")
        if (res == "Y"):
            DBManage.resetDB()
            return
        elif (res == "N"):
            return


def mockData():
    ms.createEmployee("Andrzej", "Kowalski")
    ms.createEmployee("Zdzislaw", "Skrzynecki")
    ms.createEmployee("Mariusz", "Pudzianowski")

    for i in range(1, 5):
        ms.createCard()
        clientList.append(ms.createTerminal("192.168.0.{}".format(i+100), server))
