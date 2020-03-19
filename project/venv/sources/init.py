from Server import Server
from ManagementService import ManagementService
import DBManage
from Terminal import Terminal
import sys

DBManage.initializeDB()
server = Server()
ms = ManagementService()
listOfTerminals = []
listOfCards = []

if len(sys.argv) > 1:
    if sys.argv[1] == "F":
        DBManage.resetDB()
        DBManage.initializeDB()
        ms.mockData(server)
        server.loadTerminals()
        server.loadCards()
        print("First init successful!")

terminals = ms.getAllTerminals()
cards = ms.getAllCards()

for term in terminals:
    listOfTerminals.append(Terminal(term[0], term[1]))

for card in cards:
    listOfCards.append(card[0])






