from data.requestRepository import RequestRepository
from models.request import Request
from helpers.singleton import Singleton


class RequestLogic(metaclass=Singleton):
    _repo = RequestRepository()

    # CRUD

    def create(self, request):
        self._repo.create(request)

    def read(self, user_email, date):
        return Request.from_tuple(self._repo.read(user_email, date))

    def read_all(self):
        requests = []
        for x in self._repo.read_all():
            requests.append(Request.from_tuple(x))

        return requests

    def update(self, request):
        self._repo.update(request)

    def delete(self, request):
        self._repo.delete(request)

    # NON-CRUD

    def filter(self, state="", date="", email=""):
        result = []
        for x in self._repo.read_all():

            _user_email, _date, _state = x
            if email in _user_email and f"{state}" in _state and (date == _date or date == ""):
                result.append(Request.from_tuple(x))

        return result
