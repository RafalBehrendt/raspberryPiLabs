class Action(object):
    checkIn = "Checked in an employee"
    checkOut = "Checked out an employee"
    unknown = "Unknown card registered"
    unbound = "Unbound card scanned"


TERMINAL_NOT_REGISTERED = "Terminal not registered on server"
NO_CARD_BOUND = "User has no card bound"
CARD_NOT_BOUND = "Provided card is not bound"
CLIENT_CONN = "Client connected"
CLIENT_DISCONN = "Client disconnected"

DATABASE_PATH = "../database/company.db"
CERT_PATH = "../certs/ca.crt"
HOSTNAME = "rav"
PORT_NUMBER = 8883
