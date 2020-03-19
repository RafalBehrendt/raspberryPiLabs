from Server import Server
from ManagementService import ManagementService
from Employee import Employee
import DBManage
from Terminal import Terminal

ms = ManagementService()
server = Server()
client = Terminal("123", "192.168.0.3")

DBManage.resetDB()
DBManage.initializeDB()

ms.createEmployee("Andrzej", "Klucha")
ms.createEmployee("Zdzislaw", "Splawski")
ms.createEmployee("Mariusz", "Pudzianowski")

ms.createCard()
ms.createCard()
ms.createCard()
ms.createCard()


allEmp = ms.getAllEmployees()
allCards = ms.getAllCards()

#print(allEmp)
#print(allCards)

print(ms.getLogs())

server.bindCardToEmployee(allCards[1][0], allEmp[0][0])
client.sendData(allCards[1][0], server)
client.sendData(allCards[1][0], server)

print(ms.getLogs())


#TODO: get all Employees and save them in list of employees object - will ease managing
#TODO: check how MQTT works and try to implement + Mosquito
#TODO: menu and waiting for data receieve

