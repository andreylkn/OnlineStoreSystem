from models.user.user import User


class Admin(User):
    def __init__(self, user_id, username):
        super().__init__(user_id, username)

    def add_category(self):
        name = input("Enter category name: ")
        description = input("Enter category description: ")
        if self._category_manager.add_category(name, description):
            print("Category added successfully.")
        else:
            print("Failed to add category. It may already exist.")

    def update_category(self):
        category_id = input("Enter category ID to update: ")
        name = input("Enter new category name: ")
        description = input("Enter new category description: ")
        if self._category_manager.update_category(category_id, name, description):
            print("Category updated successfully.")
        else:
            print("Category not found.")

    def delete_category(self):
        cat_id = input("Enter category ID to delete: ")
        if self._category_manager.delete_category(cat_id):
            print("Category deleted successfully.")
        else:
            print("Category not found.")

    def add_product(self):
        category_id = input("Enter category ID: ")
        name = input("Enter product name: ")
        try:
            price = float(input("Enter product price: "))
        except ValueError:
            print("Invalid price value.")
            return None
        description = input("Enter product description: ")
        try:
            discount = float(input("Enter product discount (%): "))
        except ValueError:
            print("Invalid discount value.")
            return None
        if self._product_manager.add_product(category_id, name, price, description, discount):
            print("Product added successfully.")
        else:
            print("Failed to add product.")

    def update_product(self):
        product_id = input("Enter product ID to update: ")
        category_id = input("Enter new category ID: ")
        name = input("Enter new product name: ")
        try:
            price = float(input("Enter new product price: "))
        except ValueError:
            print("Invalid price value.")
            return None
        description = input("Enter new product description: ")
        try:
            discount = float(input("Enter new product discount (%): "))
        except ValueError:
            print("Invalid discount value.")
            return None
        if self._product_manager.update_product(product_id, category_id,
                                                name, price, description, discount):
            print("Product updated successfully.")
        else:
            print("Product not found.")

    def delete_product(self):
        product_id = input("Enter product ID to delete: ")
        if self._product_manager.delete_product(product_id):
            print("Product deleted successfully.")
        else:
            print("Product not found.")


"""    def view_products_by_category(self):
        category_id = input("Enter category ID: ")
        super().view_products_by_category(category_id)"""
