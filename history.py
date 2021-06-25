import sqlite3
from sqlite3 import Error as Err


def print_table_history(conn):
    c = conn.cursor()
    req = c.execute('SELECT * FROM history')

    # print(req.fetchall())
    print("Whitelist table : ")
    for row in req.fetchall():
        print(row)
    print("\n")


def verifPath(path, conn):
    cur = conn.cursor()
    cur.execute("SELECT w.path FROM history w where path = ?;", [path])

    if cur.fetchone():
        return True
    else:
        return False


def verifId(id, conn):
    cur = conn.cursor()
    cur.execute("SELECT id FROM history where id = ?;", id)
    if cur.fetchone():
        return True
    else:
        return False


def addToHistory(name, path, conn):
    cur = conn.cursor()
    if (verifPath(path, conn)):
        print("Error add, alreay here")

    else:
        cur.execute("INSERT INTO history(path,name) VALUES(?,?);",path, name)
        conn.commit()


def deleteFromHistory(name, path, conn):
    cur = conn.cursor()
    if (verifId(id, conn)):
        cur.execute("DELETE FROM history(id) VALUES(?);", id)

    else:
        print("Error, not in the db")


# TEST
try:
    # connect to the database
    sqliteConnection = sqlite3.connect('Ransomtion-Protecware.db')
    # connect a database connection to the
    # database that resides in the memory
    dest = sqlite3.connect(':memory:')
    sqliteConnection.backup(dest)
    print("Established database connection to a database that resides in the memory!")

    print_table_history(sqliteConnection)
    addToHistory("test10", "/etc/bin/test10", sqliteConnection)

    print_table_history(sqliteConnection)  # db print

except Err:
    print(Err)

finally:
    sqliteConnection.close()


# verify if a path is already in the db

# add the name and the path of the desired process
