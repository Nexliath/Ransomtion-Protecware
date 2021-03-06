import sqlite3

class Database():
    connection = None

    def __init__(self, path="/var/lib/ransomtion-protecware/processes.db"):
        self.path = path

    def __enter__(self):
        self.connection = sqlite3.connect(self.path)
        self.init_database()

        return self.connection

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.connection.close()

    def init_database(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute("CREATE TABLE history (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, `path` VARCHAR(1024) NOT NULL, `name` TEXT NOT NULL, `reason` TEXT, `timestamp` INTEGER)")
        except sqlite3.Error:
            pass

        try:
            cursor.execute("CREATE TABLE whitelist (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, `path` VARCHAR(1024) NOT NULL, `name` TEXT NOT NULL)")
        except sqlite3.Error:
            pass

        self.connection.commit()

if __name__ == "__main__":
    with Database() as db:
        cursor = db.cursor()

        cursor.execute("SELECT `id`, `path`, `name`, `reason`, `timestamp` FROM history")
        print("History:")
        for row in cursor.fetchall():
            print(row)

        print("\nWhitelist:")
        cursor.execute("SELECT `id`, `path`, `name` FROM whitelist")
        for row in cursor.fetchall():
            print(row)

        cursor.close()
