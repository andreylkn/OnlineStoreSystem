from prettytable import PrettyTable


class Products:

    def __init__(self, product_list):
        self._product_list = product_list

    def get_product_ids(self):
        return [product[0] for product in self._product_list]

    def find_selected_product(self, selected_product):
        for prod_id in self.get_product_ids():
            if selected_product == prod_id:
                return prod_id
