from managers.base_manager import BaseManager
import sqlite3
from prettytable import PrettyTable
from datetime import datetime

from services.database import DISCOUNT, PRICE, QUANTITY
from utils.calculation_utils import calculate_effective_price, calculate_total_item_price
from utils.input_validation import input_bool

TABLE_HEADERS = ["Cart Item ID", "Product", "Quantity",
                 "Unit Price", "Discount", "Effective Unit Price", "Subtotal"]

class CartManager(BaseManager):

    def get_cart_items(self, user_id):
        cursor = self._db.connection.cursor()
        cursor.execute("""
            SELECT sc.id, p.id AS product_id, p.name, p.price, p.discount, sc.quantity 
            FROM shopping_cart sc 
            JOIN products p ON sc.product_id = p.id 
            WHERE sc.user_id = ?
        """, (user_id,))
        return cursor.fetchall()

    def show_cart_items(self, user_id):
        if items := self.get_cart_items(user_id):
            total = 0
            table = PrettyTable()
            table.field_names = TABLE_HEADERS
            for item in items:
                effective_price = calculate_effective_price(item[PRICE], item[DISCOUNT])
                item_total = calculate_total_item_price(effective_price, item[QUANTITY])
                total += item_total
                table.add_row([item["id"], item["name"], item[QUANTITY], item[PRICE], item[DISCOUNT], effective_price, item_total])
            print(table)
            print(f"Total Price: {total:.2f}")
        else:
            print("Your cart is empty.")

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

    def del_cart_item(self, cart_id):
        try:
            self._db.connection.execute("DELETE FROM shopping_cart WHERE id = ?", (cart_id,))
            self._db.connection.commit()
            print(f"Deleted Cart ID {cart_id} successfully!")
        except sqlite3.IntegrityError:
            return False

    def clear_cart(self, user_id):
        cursor = self._db.connection.cursor()
        cursor.execute("DELETE FROM shopping_cart WHERE user_id = ?", (user_id,))
        self._db.connection.commit()

    def add_sale(self, user_id, product_id, quantity, effective_price, sale_date):
        cursor = self._db.connection.cursor()
        cursor.execute(
            "INSERT INTO sales (user_id, product_id, quantity, effective_price, sale_date) VALUES (?, ?, ?, ?, ?)",
            (user_id, product_id, quantity, effective_price, sale_date)
        )
        self._db.connection.commit()

    def get_total_purchase_amount(self, items):
        total = 0
        for item in items:
            effective_price = calculate_effective_price(item[PRICE], item[DISCOUNT])
            total += calculate_total_item_price(effective_price, item[QUANTITY])

        return total

    def make_purchase(self, user_id):
        items = self.get_cart_items(user_id)
        if not items:
            print("Your cart is empty.")
        else:
            total = self.get_total_purchase_amount(items)
            print(f"Total purchase amount: {total:.2f}")

            if input_bool("Do you want to proceed with purchase?: "):
                for item in items:
                    effective_price = calculate_effective_price(item[PRICE], item[DISCOUNT])
                    sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.add_sale(user_id, item['product_id'], item[QUANTITY], effective_price, sale_date)
                self.clear_cart(user_id)
                print("Purchase successful. Your shopping cart is now empty.")
            else:
                print("Purchase cancelled.")
