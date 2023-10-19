import sqlite3


class DbContext:
    def __init__(self):
        self.connection = sqlite3.connect("data/dataBase.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS Users ("
                            "email TEXT PRIMARY KEY,"
                            "name TEXT,"
                            "u_group TEXT,"
                            "notify INT)")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS Requests ("
                            "user_email TEXT,"
                            "date DATE,"
                            "state TEXT)")

        self.connection.commit()
