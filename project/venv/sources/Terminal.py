class Terminal:

    def __init__(self, TID, address, server):
        self.TID = TID
        self.address = address
        self.server = server

    def sendData(self, CID, server):
        server.retrieveData(self.TID, CID)

    def scanCard(self, CID):
        print("Scanned card: {}".format(CID))
        self.sendData(CID, self.server)

