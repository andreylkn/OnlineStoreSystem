import unittest
from managers.category_manager import CategoryManager
from services.database import DatabaseService


class TestCategoryManager(unittest.TestCase):
    def setUp(self):
        DatabaseService._instance = None
        self.db_service = DatabaseService(":memory:")
        self.category_manager = CategoryManager()
        self.category_manager._db = self.db_service

    def test_add_and_get_category(self):
        result = self.category_manager.add_category("TestCat", "Test description")
        self.assertTrue(result)
        categories = self.category_manager.get_categories()
        # Check at least one category has the expected name.
        self.assertTrue(any(cat["name"] == "TestCat" for cat in categories))

    def test_update_category(self):
        self.category_manager.add_category("TestCat", "Test description")
        categories = self.category_manager.get_categories()
        cat_id = categories[0]["id"]
        rows_updated = self.category_manager.update_category(cat_id, "UpdatedCat", "Updated description")
        self.assertEqual(rows_updated, 1)
        categories = self.category_manager.get_categories()
        self.assertTrue(any(cat["name"] == "UpdatedCat" for cat in categories))

    def test_delete_category(self):
        self.category_manager.add_category("TestCat", "Test description")
        categories = self.category_manager.get_categories()
        cat_id = categories[0]["id"]
        rows_deleted = self.category_manager.delete_category(cat_id)
        self.assertEqual(rows_deleted, 1)


if __name__ == '__main__':
    unittest.main()
