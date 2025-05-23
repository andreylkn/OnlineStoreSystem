from prettytable import PrettyTable
from utils.print_utils import print_products_menu
from managers.base_manager import BaseManager
import sqlite3

TABLE_HEADERS = ["Product ID", "Category Name", "Product Name", "Price", "Description", "Discount"]

class ProductManager(BaseManager):
    def add_product(self, category_id, name, price, description, discount):
        try:
            self._db.connection.execute(
                "INSERT INTO products (category_id, name, price, description, discount) VALUES (?, ?, ?, ?, ?)",
                (category_id, name, price, description, discount)
            )
            self._db.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_product(self, product_id, category_id, name, price, description, discount):
        cursor = self._db.connection.cursor()
        cursor.execute(
            "UPDATE products SET category_id = ?, name = ?, price = ?, description = ?, discount = ? WHERE id = ?",
            (category_id, name, price, description, discount, product_id)
        )
        self._db.connection.commit()
        return cursor.rowcount

    def delete_product(self, product_id):
        cursor = self._db.connection.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        self._db.connection.commit()
        return cursor.rowcount

    def get_products(self):
        cursor = self._db.connection.cursor()
        cursor.execute("""
            SELECT 
                p.id AS product_id,
                p.name AS product_name,
                p.price,
                p.description,
                p.Discount,
                c.id AS category_id,
                c.name AS category_name
            FROM products p
            JOIN categories c ON p.category_id = c.id
        """)
        return cursor.fetchall()

    def show_products(self):
        table = PrettyTable()
        table.field_names = TABLE_HEADERS
        if products := self.get_products():
            for product in products:
                table.add_row([product["product_id"], product["category_name"], product["product_name"],
                               product["price"], product["description"], product["discount"]])
            print(table)
        else:
            print("No products available.")
        return products

    def get_products_by_category(self, category_id):
        cursor = self._db.connection.cursor()
        cursor.execute("""
            SELECT 
                p.id AS product_id,
                p.name AS product_name,
                p.price,
                p.description,
                p.Discount,
                c.id AS category_id,
                c.name AS category_name
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE category_id = ?
        """, (category_id,))
        return cursor.fetchall()

    def show_products_by_category(self, category_id):
        table = PrettyTable()
        table.field_names = TABLE_HEADERS
        if products := self.get_products_by_category(category_id):
            for product in products:
                table.add_row([product["product_id"], product["category_name"], product["product_name"],
                               product["price"], product["description"], product["discount"]])
            print_products_menu()
            print(table)
        else:
            print("No products available.")
        return products

    def get_product(self, product_id):
        cursor = self._db.connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        return cursor.fetchone()
