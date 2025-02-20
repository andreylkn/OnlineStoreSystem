from models.user.user import User


class Customer(User):

    _current_user_id = None

    def __init__(self, user_id, username):
        super().__init__(user_id, username)
        Customer._current_user_id = user_id

    def user_id(self):
        return self._current_user_id

