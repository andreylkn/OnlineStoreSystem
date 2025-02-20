# view list of categories, all products, products by category
# view the contents of the shopping cart
# placing products in the shopping cart
# delete products from the shopping cart
# make a purchase of the contents of the shopping cart
""" 1. view list of categories, all products, products by category
    2. view the products
    3. placing products in the shopping cart
    4. view contents of the shopping cart
    5. delete products from the shopping cart
    6. make a purchase of the contents of the shopping cart """

from services.database import DatabaseService
from models.products.category import Categories
from models.products.cart import Cart
from models.products.product import Products
from utils.print_utils import print_categories_menu, print_products_menu, print_cart_menu
from models.user.customer import Customer


# customer features: view categories, view products...
class CustomerFeatures:

    def __init__(self):
        self._db = DatabaseService()

    def view_categories(self):
        cursor = self._db.connection.cursor()
        try:
            cursor.execute("SELECT * FROM categories")
            if categories := cursor.fetchall():
                # car_list = [Car(*row) for row in cars]  # Convert each row to a Car object

                for cat in categories:
                    print({cat['name']: cat['description']})
                Categories(row[0] for row in categories)
                print_categories_menu()
                Categories(categories).display_categories()
                return categories
            else:
                print("No categories available.")
        except Exception as e:
            return f"Error: {e}"
        finally:
            cursor.close()

    def view_products(self, category_id):
        cursor = self._db.connection.cursor()
        try:
            sql = "SELECT * FROM products WHERE category_id = ?"
            cursor.execute(sql, (category_id,))
            if products := cursor.fetchall():
                Products(row[0] for row in products)
                print_products_menu()
                Products(products).display_products()
                return products
            else:
                print("No products available.")
        except Exception as e:
            return f"Error: {e}"
        finally:
            cursor.close()

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

    def view_cart(self, user_id):
        cursor = self._db.connection.cursor()
        try:
            sql = "SELECT * FROM shopping_cart WHERE user_id = ?"
            cursor.execute(sql, (user_id,))
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

    def delete_product_in_cart(self, product_id):
        cursor = self._db.connection.cursor()
        try:
            sql = "DELETE FROM shopping_cart WHERE product_id = ?"
            cursor.execute(sql, (product_id,))
            self._db.connection.commit()
            return f"Product _D:{product_id}, deleted successfully!"
        except Exception as e:
            return f"Error: {e}"
        finally:
            cursor.close()
