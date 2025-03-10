import unittest
import builtins
from managers.authorization_manager import AuthorizationManager
from services.database import DatabaseService
from services.deterministic_encryptor import DeterministicEncryptor

class TestAuthorizationManager(unittest.TestCase):
    def setUp(self):
        DatabaseService._instance = None
        self.db_service = DatabaseService(":memory:")
        self.auth_manager = AuthorizationManager()
        self.auth_manager._db = self.db_service
        self.auth_manager.community_manager._db = self.db_service
        self.auth_manager.encryptor = DeterministicEncryptor(b'1234567890123456')

        enc_username = self.auth_manager.encryptor.encrypt("testuser")
        enc_password = self.auth_manager.encryptor.encrypt("testpass")

        self.db_service.connection.execute(
            "INSERT INTO users (username, password, role, community_id, consent) VALUES (?, ?, ?, ?, ?)",
            (enc_username, enc_password, 0, None, 1)
        )
        self.db_service.connection.commit()

    def test_authenticate_success(self):
        # Simulate correct credentials
        inputs = iter(["testuser", "testpass"])
        original_input = builtins.input
        builtins.input = lambda prompt="": next(inputs)
        try:
            user = self.auth_manager.authenticate()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, "testuser")
        finally:
            builtins.input = original_input  # restore the original input

    def test_authenticate_fail(self):
        # Simulate wrong credentials
        inputs = iter(["wronguser", "wrongpass"])
        original_input = builtins.input
        builtins.input = lambda prompt="": next(inputs)
        try:
            user = self.auth_manager.authenticate()
            self.assertIsNone(user)
        finally:
            builtins.input = original_input

if __name__ == '__main__':
    unittest.main()
