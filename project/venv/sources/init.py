from Server import Server
from ManagementService import ManagementService
import DBManage
from Terminal import Terminal

DBManage.initializeDB()
server = Server()
ms = ManagementService()
listOfTerminals = []
listOfCards = []


def firstInit():
    DBManage.resetDB()
    DBManage.initializeDB()
    ms.mockData(server)
    server.loadTerminals()
    server.loadCards()
    print("First init successful!")


def init():
    cards = ms.getAllCards()

    reloadTerminals()

    for card in cards:
        listOfCards.append(card[0])


def reloadTerminals():
    listOfTerminals.clear()
    terminals = ms.getAllTerminals()

    for term in terminals:
        listOfTerminals.append(Terminal(term[0], term[1]))
