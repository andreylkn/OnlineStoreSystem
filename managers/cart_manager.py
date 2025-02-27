from managers.base_manager import BaseManager
import sqlite3
from prettytable import PrettyTable
from datetime import datetime


class CartManager(BaseManager):

    def get_carts(self, user_id):
        cursor = self._db.connection.cursor()
        cursor.execute("SELECT * FROM shopping_cart WHERE user_id = ?", (user_id,))
        return cursor.fetchall()

    def show_carts(self, user_id):
        table = PrettyTable()
        table.field_names = ["Cart ID", "User ID", "Product ID", "Quantity"]
        if carts := self.get_carts(user_id):
            for cart in carts:
                table.add_row(cart)
            print(table)
        else:
            print("Empty cart.")
        return carts

    def add_to_cart(self, user_id, product_id, quantity):
        try:
            self._db.connection.execute(
                "INSERT INTO shopping_cart (id, user_id, product_id, quantity) VALUES (?, ?, ?, ?)",
                (None, user_id, product_id, quantity)
            )
            self._db.connection.commit()
            print("Added to cart successfully!")
            return True
        except sqlite3.IntegrityError:
            return False

    def del_cart(self, cart_id):
        try:
            self._db.connection.execute("DELETE FROM shopping_cart WHERE id = ?", (cart_id,))
            self._db.connection.commit()
            print(f"Deleted Cart ID {cart_id} successfully!")
        except sqlite3.IntegrityError:
            return False

    def to_purchase(self, user_id, carts):
        try:
            for cart in carts:
                product_id = cart["product_id"]
                quantity = cart["quantity"]
                date = str(datetime.today().date())
                self._db.connection.execute("INSERT INTO sales (id, user_id, product_id, quantity, date) VALUES (?, ?,"
                                            "?, ?, ?)", (None, user_id, product_id, quantity, date))
                self._db.connection.commit()
            self._db.connection.execute("DELETE FROM shopping_cart WHERE user_id = ?", (user_id,))
            self._db.connection.commit()
            print(f"Purchase successfully!")
        except sqlite3.IntegrityError:
            return False

