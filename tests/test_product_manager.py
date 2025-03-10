import unittest
from managers.category_manager import CategoryManager
from managers.product_manager import ProductManager
from services.database import DatabaseService


class TestProductManager(unittest.TestCase):
    def setUp(self):
        DatabaseService._instance = None
        self.db_service = DatabaseService(":memory:")
        self.category_manager = CategoryManager()
        self.category_manager._db = self.db_service
        self.category_manager.add_category("TestCat", "Test description")
        categories = self.category_manager.get_categories()
        self.test_category_id = categories[0]["id"]

        self.product_manager = ProductManager()
        self.product_manager._db = self.db_service

    def test_add_and_get_product(self):
        result = self.product_manager.add_product(self.test_category_id, "TestProduct", 10.0, "Test product", 0.0)
        self.assertTrue(result)
        products = self.product_manager.get_products()
        self.assertTrue(any(prod["name"] == "TestProduct" for prod in products))

    def test_update_product(self):
        self.product_manager.add_product(self.test_category_id, "TestProduct", 10.0, "Test product", 0.0)
        products = self.product_manager.get_products()
        product_id = products[0]["id"]
        rows_updated = self.product_manager.update_product(product_id, self.test_category_id, "UpdatedProduct", 20.0, "Updated desc", 5.0)
        self.assertEqual(rows_updated, 1)
        products = self.product_manager.get_products()
        self.assertTrue(any(prod["name"] == "UpdatedProduct" for prod in products))

    def test_delete_product(self):
        self.product_manager.add_product(self.test_category_id, "TestProduct", 10.0, "Test product", 0.0)
        products = self.product_manager.get_products()
        product_id = products[0]["id"]
        rows_deleted = self.product_manager.delete_product(product_id)
        self.assertEqual(rows_deleted, 1)

if __name__ == '__main__':
    unittest.main()
