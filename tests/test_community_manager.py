import unittest
from managers.community_manager import CommunityManager
from services.database import DatabaseService


class TestCommunityManager(unittest.TestCase):
    def setUp(self):
        DatabaseService._instance = None
        self.db_service = DatabaseService(":memory:")
        self.community_manager = CommunityManager()
        self.community_manager._db = self.db_service

        cursor = self.db_service.connection.cursor()
        cursor.execute("INSERT INTO communities (name, discount) VALUES (?, ?)", ("TestCommunity", 15.0))
        community_id = cursor.lastrowid

        cursor.execute("INSERT INTO users (username, password, community_id, consent, role) VALUES (?, ?, ?, ?, ?)",
                       ("testuser", "testpass", community_id, 1, 0))
        self.user_id = cursor.lastrowid
        self.db_service.connection.commit()

    def test_get_community_discount(self):
        discount = self.community_manager.get_community_discount(self.user_id)
        self.assertEqual(discount, 15.0)


if __name__ == '__main__':
    unittest.main()
