""" 1. view list of categories, all products, products by category
    2. view the products
    3. placing products in the shopping cart
    4. view contents of the shopping cart
    5. delete products from the shopping cart
    6. make a purchase of the contents of the shopping cart """
from models.products.cart import Cart
from models.user.user import User
from services.database import DatabaseService
from utils.print_utils import print_cart_menu, print_products_menu


class Customer(User):
    def __init__(self, user_id, username):
        self._db = DatabaseService()
        super().__init__(user_id, username)

    # View list of categories
    def view_all_categories(self):
        print_cart_menu()
        return super().view_all_categories()

    # View list of products
    def view_all_products(self):
        print_products_menu()
        return super().view_all_products()

    # View the products based on the selected categories
    def view_products_from_categ(self, category_id):
        print_products_menu()
        return super().view_products_by_category(category_id)

    # Placing product in the shopping cart
    def add_to_cart(self, product_id, quantity):
        cursor = self._db.connection.cursor()
        try:
            values = (None, Customer._current_user_id, product_id, quantity)
            cursor.execute("INSERT INTO shopping_cart (id, user_id, product_id, quantity) VALUES (?, ?, ?, ?)", values)
            self._db.connection.commit()
            print("Added to cart successfully!")
            return True
        except Exception as e:
            return f"Error: {e}"
        finally:
            cursor.close()

    # View contents of the shopping cart
    def view_cart(self):
        cursor = self._db.connection.cursor()
        try:
            sql = "SELECT * FROM shopping_cart WHERE user_id = ?"
            cursor.execute(sql, (self.id,))
            if carts := cursor.fetchall():
                Cart(row[0] for row in carts)
                print_cart_menu()
                Cart(carts).display_cart()
                return carts
            else:
                print("No products available.")
            return True
        except Exception as e:
            return f"Error: {e}"
        finally:
            cursor.close()

    # Delete selected cart_id from the shopping cart
    def del_prod_in_cart(self, cart_id):
        cursor = self._db.connection.cursor()
        try:
            sql = "DELETE FROM shopping_cart WHERE id = ?"
            cursor.execute(sql, (cart_id,))
            self._db.connection.commit()
            print(f"Cart ID:{cart_id}, deleted successfully!")
            return True
        except Exception as e:
            return f"Error: {e}"
        finally:
            cursor.close()
