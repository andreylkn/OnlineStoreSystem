from models.user.user import User
from services.database import DatabaseService
from utils.print_utils import print_cart_menu, print_products_menu, print_categories_menu


class Customer(User):
    def __init__(self, user_id, username):
        super().__init__(user_id, username)

    # View list of categories
    def view_all_categories(self):
        print_categories_menu()
        return super().view_all_categories()

    # View list of products
    def view_all_products(self):
        print_products_menu()
        return super().view_all_products()

    # View contents of the shopping cart
    def view_cart(self):
        print_cart_menu()
        return self._cart_manager.show_cart_items(self.id)

    # Placing product in the shopping cart
    def add_to_cart(self):
        product_id = input("Enter product ID: ")
        quantity = input("Enter quantity: ")
        return self._cart_manager.add_to_cart(self.id, product_id, quantity)

    # Delete selected cart_id from the shopping cart
    def del_prod_in_cart(self):
        cart_id = input("Enter Cart ID to remove the product from your cart: ")
        return self._cart_manager.del_cart_item(cart_id)

    # To make a purchase (Everything in Carts)
    def make_purchase(self):
        self._cart_manager.make_purchase(self.id)
