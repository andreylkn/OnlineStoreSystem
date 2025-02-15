import sqlite3

# Constants for a user table
ROLE = 'role'
USER_ID = 'id'
USERNAME = 'username'
PASSWORD = 'password'

class DatabaseService:
    def __init__(self, db_name="store.db"):
        self._connection = sqlite3.connect(db_name)
        self._connection.row_factory = sqlite3.Row
        self._initialize_tables()

    @property
    def connection(self):
        return self._connection

    def _initialize_tables(self):
        cursor = self._connection.cursor()
        self._create_tables(cursor)
        self._connection.commit()

    def _create_tables(self, cursor):
        self._create_users_table(cursor)
        self._create_categories_table(cursor)
        self._create_products_table(cursor)
        self._create_shopping_cart_table(cursor)

    def _create_users_table(self, cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role INTEGER
            )
        """)

    def _create_categories_table(self, cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                description TEXT
            )
        """)

    def _create_products_table(self, cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER,
                name TEXT,
                price REAL,
                description TEXT,
                discount REAL,
                FOREIGN KEY(category_id) REFERENCES categories(id)
            )
        """)

    def _create_shopping_cart_table(self, cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shopping_cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(product_id) REFERENCES products(id)
            )
        """)
