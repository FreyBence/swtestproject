from data.dataContext import DbContext
from helpers.singleton import Singleton


class UserRepository(metaclass=Singleton):
    _ctx = DbContext()

    def create(self, user):
        self._ctx.cursor.execute("INSERT INTO Users( email, name, u_group, notify)"
                                 "VALUES(?,?,?,?)",
                                 (user.email, user.name, user.group, user.notify))
        self._ctx.cursor.fetchone()
        self._ctx.connection.commit()

    def read(self, email):
        self._ctx.cursor.execute("SELECT * FROM Users WHERE email=?", (email,))
        return self._ctx.cursor.fetchone()

    def read_all(self):
        self._ctx.cursor.execute("SELECT * FROM Users")
        return self._ctx.cursor.fetchall()

    def update(self, user):
        self._ctx.cursor.execute("UPDATE Users SET name=?, u_group=?, notify=? WHERE email=? ",
                                 (user.name, user.group, user.notify, user.email))
        self._ctx.cursor.fetchone()
        self._ctx.connection.commit()

    def delete(self, user):
        self._ctx.cursor.execute("DELETE FROM Users WHERE email=?", (user.email,))
        self._ctx.cursor.fetchone()
        self._ctx.connection.commit()
