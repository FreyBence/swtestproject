from data.userRepository import UserRepository
from models.user import User
from helpers.singleton import Singleton


class UserLogic(metaclass=Singleton):
    _repo = UserRepository()

    # CRUD

    def create(self, user):
        if len(self.read_all()) == 0:
            user.group = "administrator"
        self._repo.create(user)

    def read(self, email):
        return User.from_tuple(self._repo.read(email))

    def read_all(self):
        users = []
        for x in self._repo.read_all():
            users.append(User.from_tuple(x))

        return users

    def update(self, user):
        self._repo.update(user)

    def delete(self, user):
        self._repo.delete(user)

    # NON-CRUD

    def filter(self, email="", name="", group=""):
        result = []
        for x in self._repo.read_all():
            _email, _name, _group, _notify = x
            if email in _email and name in _name and f"{group}" in _group:
                result.append(User.from_tuple(x))

        return result

    def get_user_of_request(self, request):
        return self._repo.read(request.user_email)

    def get_notifyd_users(self):
        result = []
        for x in self._repo.read_all():
            _email, _name, _group, _notify = x
            if _notify == 1:
                result.append(User.from_tuple(x).notify)
