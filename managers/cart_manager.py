from managers.base_manager import BaseManager
import sqlite3
import uuid
from prettytable import PrettyTable
from datetime import datetime

from managers.community_manager import CommunityManager
from services.database import DISCOUNT, PRICE, QUANTITY, EFFECTIVE_PRICE, SALE_DATE, PURCHASE_ID
from utils.calculation_utils import calculate_effective_price, calculate_total_item_price
from utils.input_validation import input_bool

TABLE_HEADERS = ["Cart Item ID", "Product", "Quantity",
                 "Unit Price", "Discount", "Effective Unit Price", "Subtotal"]

PURCHASE_HISTORY_TABLE_HEADERS = ["Purchase ID", "Product ID", "Quantity", "Effective Price", "Date"]


class CartManager(BaseManager):
    def __init__(self):
        super().__init__()
        self._community_manager = CommunityManager()

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
            community_discount = self._community_manager.get_community_discount(user_id)
            total = 0
            table = PrettyTable()
            table.field_names = TABLE_HEADERS
            for item in items:
                effective_price = calculate_effective_price(item[PRICE], item[DISCOUNT], community_discount)
                item_total = calculate_total_item_price(effective_price, item[QUANTITY])
                total += item_total
                table.add_row([item["id"], item["name"], item[QUANTITY], item[PRICE], item[DISCOUNT], "{:.2f}".format(effective_price), "{:.2f}".format(item_total)])
            print(table)
            if community_discount != 0:
                print(f"Community Discount: {community_discount}%")
            print(f"Total Price: {total:.2f}")
        else:
            print("Your cart is empty.")

    def add_to_cart(self, user_id, product_id, quantity):
        try:
            cursor = self._db.connection.cursor()
            cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))

            if cursor.fetchone():
                self._db.connection.execute(
                    "INSERT INTO shopping_cart (id, user_id, product_id, quantity) VALUES (?, ?, ?, ?)",
                    (None, user_id, product_id, quantity)
                )
                self._db.connection.commit()
                print("Added to cart successfully!")
            else:
                print("Invalid product ID.")
            return True
        except sqlite3.IntegrityError:
            return False

    def del_cart_item(self, user_id, cart_id):
        try:
            cursor = self._db.connection.cursor()
            cursor.execute("SELECT 1 FROM shopping_cart WHERE id = ? AND user_id = ?", (cart_id, user_id))
            if cursor.fetchone() is None:
                print(f"Cart ID {cart_id} does not exist in the your Cart.")
                return False
            self._db.connection.execute("DELETE FROM shopping_cart WHERE id = ? AND user_id = ?", (cart_id, user_id))
            self._db.connection.commit()
            print(f"Deleted Cart ID {cart_id} successfully!")
        except sqlite3.IntegrityError:
            return False

    def clear_cart(self, user_id):
        cursor = self._db.connection.cursor()
        cursor.execute("DELETE FROM shopping_cart WHERE user_id = ?", (user_id,))
        self._db.connection.commit()

    def add_sale(self, purchase_id, user_id, product_id, quantity, effective_price, sale_date):
        cursor = self._db.connection.cursor()
        cursor.execute(
            "INSERT INTO sales (purchase_id, user_id, product_id, quantity, effective_price, sale_date) VALUES (?, ?, ?, ?, ?, ?)",
            (purchase_id, user_id, product_id, quantity, effective_price, sale_date)
        )
        self._db.connection.commit()

    def get_total_purchase_amount(self, items, community_discount):
        total = 0
        for item in items:
            effective_price = calculate_effective_price(item[PRICE], item[DISCOUNT], community_discount)
            total += calculate_total_item_price(effective_price, item[QUANTITY])
        return total

    def make_purchase(self, user_id, is_store_data_allowed):
        items = self.get_cart_items(user_id)
        if not items:
            print("Your cart is empty.")
        else:
            community_discount = self._community_manager.get_community_discount(user_id)
            total = self.get_total_purchase_amount(items, community_discount)
            print(f"Total purchase amount: {total:.2f}")

            if input_bool("Do you want to proceed with purchase?: "):
                purchase_id = str(uuid.uuid4())
                saved_user_id = user_id if is_store_data_allowed else None
                for item in items:
                    effective_price = calculate_effective_price(item[PRICE], item[DISCOUNT], community_discount)
                    sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.add_sale(purchase_id, saved_user_id, item['product_id'], item[QUANTITY], effective_price, sale_date)
                self.clear_cart(user_id)
                print("Purchase successful. Your shopping cart is now empty.")
            else:
                print("Purchase cancelled.")

    def get_purchase_history(self, userID):
        try:
            cursor = self._db.connection.cursor()
            cursor.execute(
                "SELECT purchase_id, product_id, quantity, effective_price, sale_date FROM sales WHERE user_id = ?", (userID,))
            purchase_history_list = cursor.fetchall()
            if len(purchase_history_list) == 0:
                print("There is no record of any purchase history.")
            else:
                table = PrettyTable()
                table.field_names = PURCHASE_HISTORY_TABLE_HEADERS
                for item in purchase_history_list:
                    table.add_row([item[PURCHASE_ID], item["product_id"], item[QUANTITY], f"{item[EFFECTIVE_PRICE]:.2f}", item[SALE_DATE]])

                print(table)
        except sqlite3.IntegrityError:
            return False



