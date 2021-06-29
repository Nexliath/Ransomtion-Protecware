import sqlite3
from sqlite3 import Error as Err


def print_table_whitelist(conn):
    c = conn.cursor()
    req = c.execute('SELECT * FROM whitelist')

    # print(req.fetchall())
    print("Whitelist table : ")
    for row in req.fetchall():
        print(row)
    print("\n")


def verifPath(path, conn):
    cur = conn.cursor()
    cur.execute("SELECT w.path FROM whitelist w where path = ?;", [path])

    if cur.fetchone():
        return True
    else:
        return False


def verifId(id, conn):
    cur = conn.cursor()
    cur.execute("SELECT id FROM whitelist where id = ?;", id)
    if cur.fetchone():
        return True
    else:
        return False


def addToWhitelist(name, path, conn):
    cur = conn.cursor()
    if (verifPath(path, conn)):
        print("Error add, alreay here")

    else:
        cur.execute("INSERT INTO whitelist(path,name) VALUES(?,?);",
                    ((path), (name)))
        conn.commit()


def deleteFromWhitelist(id, conn):
    cur = conn.cursor()

    if (verifId(id, conn)):
        cur.execute("DELETE FROM whitelist WHERE id =?;",id)
        conn.commit()
    else:
        print("Error, not in the db")


# TEST
try:
    # connect to the database
    sqliteConnection = sqlite3.connect('Ransomtion-Protecware.db')
    print("Database connection is established successfully!")

    # connect a database connection to the
    # database that resides in the memory
    dest = sqlite3.connect(':memory:')
    sqliteConnection.backup(dest)
    print("Established database connection to a database that resides in the memory!")

    print_table_whitelist(sqliteConnection)
    print(verifPath("/usr/local/bin/test8", sqliteConnection))

    addToWhitelist("test10", "/etc/bin/test10", sqliteConnection)

    print_table_whitelist(sqliteConnection)  # db print

except Err:
    print(Err)

finally:
    sqliteConnection.close()


# verify if a path is already in the db

# add the name and the path of the desired process
