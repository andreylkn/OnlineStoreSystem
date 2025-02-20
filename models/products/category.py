from prettytable import PrettyTable


class Categories:

    def __init__(self, category_list):
        self._category_list = category_list

    """@property
    def id(self):
        return self._id

    @property
    def categories_name(self):
        return self._cats_name

    @property
    def cats_description(self):
        return self._cats_description"""

    def display_categories(self):
        table = PrettyTable()
        table.field_names = ["Number", "Category", "Description"]
        for category in self._category_list:
            table.add_row(category)
        print(table)

    def get_category_ids(self):
        return [category[0] for category in self._category_list]

    def find_selected_category(self, selected_category):
        for cat_id in self.get_category_ids():
            if selected_category == cat_id:
                return cat_id
