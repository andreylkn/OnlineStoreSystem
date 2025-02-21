from managers.category_manager import CategoryManager
from managers.product_manager import ProductManager

class User:
    def __init__(self, _user_id, username):
        self._id = _user_id
        self._username = username
        self._category_manager = CategoryManager()
        self._product_manager = ProductManager()

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    def view_all_categories(self):
        return self._category_manager.show_all_category()

    def view_all_products(self):
        self._product_manager.show_products()

    def view_products_by_category(self, category_id):
        self._product_manager.show_products_by_category(category_id)