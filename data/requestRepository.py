from data.dataContext import DbContext
from helpers.singleton import Singleton


class RequestRepository(metaclass=Singleton):
    _ctx = DbContext()

    def create(self, request):
        self._ctx.cursor.execute("INSERT INTO Requests(user_email, date, state)"
                                 "VALUES(?,date(?),?)",
                                 (request.user_email, request.date, request.state))
        self._ctx.cursor.fetchone()
        self._ctx.connection.commit()

    def read(self, user_email, date):
        self._ctx.cursor.execute("SELECT * FROM Requests WHERE user_email=? AND date=?",
                                 (user_email, date))
        return self._ctx.cursor.fetchone()

    def read_all(self):
        self._ctx.cursor.execute("SELECT * FROM Requests")
        return self._ctx.cursor.fetchall()

    def update(self, request):
        self._ctx.cursor.execute("UPDATE Requests SET state=? WHERE user_email=? AND date=?",
                                 (request.state, request.user_email, request.date))
        self._ctx.cursor.fetchone()
        self._ctx.connection.commit()

    def delete(self, request):
        self._ctx.cursor.execute("DELETE FROM Requests WHERE user_email=? AND date=?",
                                 (request.user_email, request.date))
        self._ctx.cursor.fetchone()
        self._ctx.connection.commit()
