import unittest
from managers.cart_manager import CartManager
from managers.community_manager import CommunityManager
from services.database import DatabaseService


class TestCartManager(unittest.TestCase):
    def setUp(self):
        DatabaseService._instance = None
        self.db_service = DatabaseService(":memory:")

        # Create a category first because product requires a valid category_id.
        cursor = self.db_service.connection.cursor()
        cursor.execute("INSERT INTO categories (name, description) VALUES (?, ?)", ("TestCat", "Test description"))
        cat_id = cursor.lastrowid

        # Insert a test user.
        cursor.execute("INSERT INTO users (username, password, community_id, consent, role) VALUES (?, ?, ?, ?, ?)",
                       ("testuser", "testpass", None, 1, 0))
        self.user_id = cursor.lastrowid

        # Insert a test product.
        cursor.execute("INSERT INTO products (category_id, name, price, description, discount) VALUES (?, ?, ?, ?, ?)",
                       (cat_id, "TestProduct", 50.0, "Test product description", 10.0))
        self.product_id = cursor.lastrowid
        self.db_service.connection.commit()

        self.cart_manager = CartManager()
        self.cart_manager._db = self.db_service

        self.cart_manager._community_manager = CommunityManager()
        self.cart_manager._community_manager._db = self.db_service

    def test_add_to_cart(self):
        result = self.cart_manager.add_to_cart(self.user_id, self.product_id, 2)
        self.assertTrue(result)
        items = self.cart_manager.get_cart_items(self.user_id)
        self.assertEqual(len(items), 1)

    def test_del_cart_item(self):
        self.cart_manager.add_to_cart(self.user_id, self.product_id, 2)
        items = self.cart_manager.get_cart_items(self.user_id)
        cart_id = items[0]["id"]
        self.cart_manager.del_cart_item(self.user_id, cart_id)
        items_after = self.cart_manager.get_cart_items(self.user_id)
        self.assertEqual(len(items_after), 0)

if __name__ == '__main__':
    unittest.main()
