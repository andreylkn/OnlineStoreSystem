from managers.community_manager import CommunityManager
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
        self.community_manager = CommunityManager()


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
        role = ADMIN_ROLE if is_admin is True else CUSTOMER_ROLE

        community_id = None
        if role == CUSTOMER_ROLE:
            print("\nDo you belong to any of the following communities?")
            self.community_manager.show_communities()
            if input_bool(""):
                selected_community = int(input("Enter the community ID: "))
                communities = self.community_manager.get_communities()

                # Verify selected community exists
                if selected_community and any(comm['id'] == selected_community for comm in communities):
                    community_id = selected_community
                else:
                    print("Invalid community ID. No discount will be applied.")
        self.__register(username, password, role, community_id)


    def __register(self, username, password, role=CUSTOMER_ROLE, community_id=None):
        # Hash password
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            self._db.connection.execute(
                "INSERT INTO users (username, password, role, community_id) VALUES (?, ?, ?, ?)",
                (username, hashed_pw.decode('utf-8'), role, community_id)
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
