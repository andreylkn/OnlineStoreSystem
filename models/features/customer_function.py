# view list of categories, all products, products by category
# view the contents of the shopping cart
# placing products in the shopping cart
# delete products from the shopping cart
# make a purchase of the contents of the shopping cart

from services.database import DatabaseService


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

            else:
                print("No categories available.")
        finally:
            cursor.close()


    def view_products(self, category_id):
        cursor = self._db.connection.cursor()
        try:
            sql = "SELECT * FROM products WHERE category_id = ?"
            cursor.execute(sql, category_id)
            if products := cursor.fetchall():
                # car_list = [Car(*row) for row in cars]  # Convert each row to a Car object

                for product in products:
                    print({product['name']: product['price']})

            else:
                print("No categories available.")
        except:
            return False
