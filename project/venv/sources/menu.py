import sys


class Menu:
    currentCard = None
    currentEmployee = None
    currentTerminal = None
    listOfCommands = []

    def dropDB(self):  # drops database
        from main import ms, server, listOfTerminals, listOfCards
        isDropped = ms.dropDB()
        if isDropped:
            ms.initDB()
            server.__init__()
            listOfTerminals.clear()
            listOfCards.clear()
            self.currentCard = None
            self.currentTerminal = None
            self.currentEmployee = None

    def shc(self):  # shows current card
        print(self.currentCard)

    def she(self):  # shows current employee
        from main import ms
        if self.currentEmployee is not None:
            emp = ms.getEmployeeById(self.currentEmployee)
            print(emp.toString())
        else:
            print(None)

    def sht(self, ):  # shows current terminal
        if self.currentTerminal is not None:
            print(self.currentTerminal.toString())
        else:
            print(None)

    def shemps(self):  # shows all employees
        from main import ms
        ms.printAllEmployees()

    def shcards(self):  # shows all cards
        from main import ms
        ms.printCards()

    def shterms(self):  # shows all terminals
        from main import ms
        ms.printAllTerminals()

    def shrcards(self):  # shows all registered cards
        from main import server
        for card in server.listOfCards:
            print(card)

    def shrterms(self):  # shows all registered terminals
        from main import server
        for term in server.listOfTerminals:
            print(term)

    def shLogs(self):  # shows all logs
        from main import ms
        ms.printLogs()

    def chc(self, x):  # changes current card to x in list of cards
        from main import ms
        from main import listOfCards
        if x < 0 or x >= len(listOfCards):
            print("Desired card is not available\n Available cards:")
            ms.printCards()
            return
        self.currentCard = listOfCards[x]
        print("Changed current card to")

        self.shc()

    def che(self, x):  # changes current Employee to x in list of employees
        from main import ms
        emps = ms.getAllEmployees()
        if x < 0 or x >= len(emps):
            print("Desired employee is not available\n Available employees:")
            ms.printAllEmployees()
            return
        self.currentEmployee = emps[x][0]
        emp = ms.getEmployeeById(self.currentEmployee)
        print("Changed current employee to")
        self.she()

    def cht(self, x):  # changes current Terminal to x in list of terminals
        from main import listOfTerminals
        if x < 0 or x >= len(listOfTerminals):
            print("Desired terminal is not available\n Available terminals:")
            for term in listOfTerminals:
                print(term.toString())
            return
        self.currentTerminal = listOfTerminals[x]
        print("Changed current terminal to")
        self.sht()

    def btu(self):  # binds current card to user
        from main import server
        if self.currentEmployee is not None and self.currentCard is not None:
            server.bindCardToEmployee(self.currentCard, self.currentEmployee)
        else:
            print("Cannot bind card {} to employee {}".format(self.currentCard, self.currentEmployee))

    def ubtu(self):  # unbinds current card from user
        from main import server
        if self.currentCard is not None:
            server.unbindCardFromEmployee(self.currentCard)
        else:
            print("Cannot unbind card {}".format(self.currentCard))

    def rt(self):  # registers current terminal on server
        from main import server
        if self.currentTerminal is not None:
            server.registerTerminal(self.currentTerminal.TID)
            print("Registered terminal")
        else:
            print("Current terminal is not valid")

    def urt(self):  # unregisters current terminal from server
        from main import server
        if self.currentTerminal is not None:
            server.unregisterTerminal(self.currentTerminal.TID)
            print("Unregistered terminal")
        else:
            print("Current terminal is not valid")

    def scan(self):  # scan current card
        if self.currentCard is not None:
            self.currentTerminal.scanCard(self.currentCard)
        else:
            print("Current card is not valid")

    def report(self):  # creates report fot current employee
        from main import server
        if self.currentEmployee is not None:
            server.generateReport(self.currentEmployee)
        else:
            print("Current employee is not valid")

    def exit(self):  # exits app
        sys.exit()

    def start(self):
        self.chc(0)
        self.che(0)
        self.cht(0)

        while True:
            comm = input("> ")
            try:
                exec("self." + comm)
            except SystemExit:
                sys.exit()
            except:
                print("Unknown command")
