from managers.base_manager import BaseManager
from prettytable import PrettyTable
from dbm import sqlite3

class CategoryManager(BaseManager):
    def add_category(self, name, description):
        try:
            self._db.connection.execute(
                "INSERT INTO categories (name, description) VALUES (?, ?)",
                (name, description)
            )
            self._db.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_category(self, category_id, name, description):
        cursor = self._db.connection.cursor()
        cursor.execute(
            "UPDATE categories SET name = ?, description = ? WHERE id = ?",
            (name, description, category_id)
        )
        self._db.connection.commit()
        return cursor.rowcount

    def delete_category(self, category_id):
        cursor = self._db.connection.cursor()
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        self._db.connection.commit()
        return cursor.rowcount

    def get_categories(self):
        cursor = self._db.connection.cursor()
        cursor.execute("SELECT * FROM categories")
        return cursor.fetchall()

    def show_all_category(self):
        table = PrettyTable()
        table.field_names = ["Number", "Category", "Description"]
        if categories := self.get_categories():
            for category in categories:
                table.add_row(category)
            print(table)
        else:
            print("No categories available.")
        return categories
