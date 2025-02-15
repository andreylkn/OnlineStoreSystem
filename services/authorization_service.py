from models.user.admin import Admin
from models.user.customer import Customer
from services.database import ROLE, USER_ID, USERNAME, PASSWORD, DatabaseService
from utils.input_validation import input_bool
import bcrypt

ADMIN_ROLE = 1 #admin
CUSTOMER_ROLE = 2 #customer

class AuthorizationService:
    def __init__(self):
        self._db = DatabaseService()

    def authenticate(self):
        username = input("Username: ")
        password = input("Password: ")

        user_data = self.__login(username, password)
        if not user_data:
            print("Invalid credentials.")
            return None
        if user_data[ROLE] == ADMIN_ROLE:
            return Admin(user_data[USER_ID], user_data[USERNAME])
        else:
            return Customer(user_data[USER_ID], user_data[USERNAME])

    def register_user(self):
        username = input("Choose a username: ")
        password = input("Choose a password: ")

        is_admin = input_bool("Are you an admin?: ")
        role = ADMIN_ROLE if is_admin == True else CUSTOMER_ROLE
        if self.__register(username, password, role):
            print("User registered successfully.")
        else:
            print("Registration failed. Username might be taken.")

    def __register(self, username, password, role=CUSTOMER_ROLE):
        # Hash password
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            self._db.connection.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, hashed_pw.decode('utf-8'), role)
            )
            self._db.connection.commit()
            return True
        except:
            return False

    def __login(self, username, password):
        cursor = self._db.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[PASSWORD].encode('utf-8')):
            return user
        return None
