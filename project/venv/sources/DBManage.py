import sqlite3


def initializeDB():
    conn = sqlite3.connect('../database/company.db')

    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS employees (
        EID text PRIMARY KEY NOT NULL,
        name text,
        surnmae text
    )""")

    conn.commit()

    c.execute("""CREATE TABLE IF NOT EXISTS logs (
        CID text NOT NULL,
        TID text,
        EID text,
        action text,
        datetime timestamp
    )""")

    conn.commit()

    c.execute("""CREATE TABLE IF NOT EXISTS cards (
    CID text
    )""")

    conn.commit()

    c.execute("""CREATE TABLE IF NOT EXISTS terminals (
        TID text,
        address text
    )""")

    conn.commit()

    c.execute("""CREATE TABLE IF NOT EXISTS bindings (
        EID text,
        CID text
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
