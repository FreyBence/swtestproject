class User:
    def __init__(self, email, name, group="viewer", notify=0):
        self.email = email
        self.name = name
        self.group = group
        self.notify = notify

    @classmethod
    def from_tuple(cls, data):
        if data is None:
            return None
        email, name, group, notify = data
        return cls(email=email, name=name, group=group, notify=notify)
