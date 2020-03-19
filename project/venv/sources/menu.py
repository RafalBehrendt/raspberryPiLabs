def startMenu():
    currentCard = 0
    currentEmployee = 0
    currentTerminal = 0
    running = True

    def dropDB():  # drops database
        from init import dropDB
        dropDB()

    def showCard():  # shows current card
        print(currentCard)

    def showEmp():  # shows current employee
        from init import ms
        emp = ms.getEmployeeById(currentEmployee)
        print(emp.toString())

    def showTerm(): # shows current terminal
        print(currentTerminal)

    def chCard(x):  # changes current card to x in list of cards
        from init import server
        from init import ms
        if x < 0 or x >= len(server.listOfCards):
            print("Desired card is not available\n Available cards:")
            ms.printCards()
            return
        currentCard = server.listOfCards[x]

    def chEmp(x):  # changes current Employee to x in list of employees
        from init import ms
        emps = ms.getAllEmployees()
        if x < 0 or x >= len(emps):
            print("Desired employee is not available\n Available employees:")
            ms.printAllEmployees()
            return
        currentEmployee = emps[x][0]

    def chTerm(x): # change current Terminal
        from init import clientList
        if x < 0 or x >= len(clientList):
            print("Desired terminal is not available\n Available terminals:")
            print(clientList)
            return
        currentTerminal = clientList[x]


    def btu():  # binds current card to user
        from init import server
        server.bindCardToEmployee(currentCard, currentEmployee)

    def scan():  # scan current card
        from Terminal import Terminal
        curTerm : Terminal = currentTerminal
        curTerm.scanCard(currentCard)

    def exit(): # exits app
        running = False

    chCard(0)
    chEmp(0)
    chTerm(0)

    while running:
        comm = input("> ")
        exec(comm)
        print(running) #mf is diffrent than global ig
