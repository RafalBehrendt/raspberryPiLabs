from Server import Server

class Terminal:

    def __init__(self, TID, address):
        self.TID = TID
        self.address = address

    def sendData(self, CID, server : Server):
        server.retrieveData(self.TID, CID)

    def scanCard(self, CID):
        print("Zeskanowano karte: {}".format(CID))

