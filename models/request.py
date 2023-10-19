class Request:
    def __init__(self, user_email, date, state="pending"):
        self.user_email = user_email
        self.date = date
        self.state = state

    @classmethod
    def from_tuple(cls, data):
        if data is None:
            return None
        user_email, date, state = data
        return cls(user_email=user_email, date=date, state=state)
