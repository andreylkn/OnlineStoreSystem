from managers.community_manager import CommunityManager
from models.user.admin import Admin
from models.user.customer import Customer
from services.database import ROLE, USER_ID, USERNAME, PASSWORD, DatabaseService, CONSENT
from services.deterministic_encryptor import DeterministicEncryptor, ENCRYPTION_KEY
from utils.input_validation import input_bool

ADMIN_ROLE = 1 #admin
CUSTOMER_ROLE = 2 #customer

class AuthorizationManager:
    def __init__(self):
        self._db = DatabaseService()
        self.community_manager = CommunityManager()
        self.encryptor = DeterministicEncryptor(ENCRYPTION_KEY)

    def authenticate(self):
        username = input("Username: ")
        password = input("Password: ")

        user_data = self.__login(username, password)
        if not user_data:
            print("Invalid credentials.")
            return None

        if user_data[ROLE] == ADMIN_ROLE:
            return Admin(user_data[USER_ID], username)
        else:
            return Customer(user_data[USER_ID], username, user_data[CONSENT])


    def register_user(self):
        username = input("Choose a username: ")
        if not username:
            print("Error: Username cannot be empty. Registration aborted.")
            return None

        password = input("Choose a password: ")
        if not password:
            print("Error: Password cannot be empty. Registration aborted.")
            return None

        is_admin = input_bool("Are you an admin?: ")
        role = ADMIN_ROLE if is_admin is True else CUSTOMER_ROLE

        consent = None
        community_id = None
        if role == CUSTOMER_ROLE:
            consent_input = input_bool("\nMay we collect your data for purchase history?")
            consent = 1 if consent_input is True else 0

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
        self.__register(username, password, role, community_id, consent)


    def __register(self, username, password, role=CUSTOMER_ROLE, community_id=None, consent=False):
        # Hash password
        encrypted_password = self.encryptor.encrypt(password)
        encrypted_username = self.encryptor.encrypt(username)
        try:
            self._db.connection.execute(
                "INSERT INTO users (username, password, role, community_id, consent) VALUES (?, ?, ?, ?, ?)",
                (encrypted_username, encrypted_password, role, community_id, consent)
            )
            self._db.connection.commit()
            print("Registration Successful!")
            return True
        except:
            print("Registration Failed.")
            return False


    def __login(self, username, password):
        cursor = self._db.connection.cursor()
        encrypted_password = self.encryptor.encrypt(username)
        encrypted_username = self.encryptor.encrypt(password)
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                       (encrypted_password, encrypted_username))
        return cursor.fetchone()
