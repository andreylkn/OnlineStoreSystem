class User:
    def __init__(self, _user_id, username):
        self._id = _user_id
        self._username = username

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username
