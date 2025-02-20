from prettytable import PrettyTable


class Cart:

    def __init__(self, cart_list):
        self._cart_list = cart_list

    def display_cart(self):
        table = PrettyTable()
        table.field_names = ["Cart ID", "User ID", "Product ID", "Quantity"]
        for cart in self._cart_list:
            table.add_row(cart)
        print(table)

    def get_cart_ids(self):
        return [cart[0] for cart in self._cart_list]

    def find_selected_cart(self, selected_cart):
        for cart_id in self.get_cart_ids():
            if selected_cart == cart_id:
                return cart_id
