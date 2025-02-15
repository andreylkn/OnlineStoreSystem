from models.user.user import User

class Customer(User):
    def __init__(self, user_id, username):
        super().__init__(user_id, username)
