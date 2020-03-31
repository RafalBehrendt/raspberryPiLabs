import sqlite3


def initializeDB():
    conn = sqlite3.connect('../database/company.db')

    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS employees (
        EID text PRIMARY KEY NOT NULL,
        name text,
        surname text
    )""")

    conn.commit()

    c.execute("""CREATE TABLE IF NOT EXISTS cards (
        CID text PRIMARY KEY NOT NULL,
        isRegistered integer,
        EID text,
        FOREIGN KEY(EID) REFERENCES employees(EID)
    )""")

    conn.commit()

    c.execute("""CREATE TABLE IF NOT EXISTS terminals (
        TID text PRIMARY KEY NOT NULL,
        address text,
        isRegistered integer
    )""")

    conn.commit()

    c.execute("""CREATE TABLE IF NOT EXISTS logs (
        CID text,
        TID text,
        EID text,
        action text,
        datetime timestamp,
        FOREIGN KEY(CID) REFERENCES cards(CID),
        FOREIGN KEY(TID) REFERENCES terminals(TID),
        FOREIGN KEY(EID) REFERENCES employees(EID)
    )""")

    conn.commit()
    conn.close()


def resetDB():
    conn = sqlite3.connect('../database/company.db')
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS employees")
    c.execute("DROP TABLE IF EXISTS logs")
    c.execute("DROP TABLE IF EXISTS cards")
    c.execute("DROP TABLE IF EXISTS terminals")
    c.execute("DROP TABLE IF EXISTS bindings")
    c.execute("DROP TABLE IF EXISTS registeredTerminals")
    initializeDB()
