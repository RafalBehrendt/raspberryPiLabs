class Terminal:

    def __init__(self, TID, address):
        self.TID = TID
        self.address = address

    def sendData(self, CID, server):
        server.retrieveData(self.TID, CID)

    def scanCard(self, CID):
        from main import server
        print("Scanned card: {}".format(CID))
        self.sendData(CID, server)

    def toString(self):
        return "TID: {} \naddress: {}".format(self.TID, self.address)

