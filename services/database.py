import sqlite3

# Constants for a user table
ROLE = 'role'
USER_ID = 'id'
USERNAME = 'username'
PASSWORD = 'password'

# Constants for categories and products
PRODUCT_ID = 'id'
NAME = 'name'
DESCRIPTION = 'description'
CATEGORY = 'category'
PRICE = 'price'
DISCOUNT = 'discount'

class DatabaseService:
    _instance = None

    def __new__(cls):
        #Singleton
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_name="store.db"):
        # To avoid reinitializing,
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._connection = sqlite3.connect(db_name)
        self._connection.row_factory = sqlite3.Row
        self._initialize_tables()
        self._initialized = True

    @property
    def connection(self):
        return self._connection

    def _initialize_tables(self):
        self._create_tables()
        if self._is_empty():
            self._seed_test_data()
        self._connection.commit()

    def _create_tables(self):
        cursor = self._connection.cursor()
        self._create_users_table(cursor)
        self._create_categories_table(cursor)
        self._create_products_table(cursor)
        self._create_shopping_cart_table(cursor)
        self._create_sales_table(cursor)

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

    def _create_sales_table(self, cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                date TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(product_id) REFERENCES products(id)
            )
        """)

    def _is_empty(self):
        """Checks if the categories table is empty."""
        cursor = self._connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM categories")
        count = cursor.fetchone()[0]
        return count == 0

    def _seed_test_data(self):
        cursor = self._connection.cursor()
        self._seed_categories_data(cursor)
        self._seed_products_data(cursor)

    def _seed_categories_data(self, cursor):
        # Insert test categories
        categories = [
            {NAME: 'Electronics', DESCRIPTION: 'Electronic gadgets and devices'},
            {NAME: 'Books', DESCRIPTION: 'Various kinds of books'},
            {NAME: 'Clothing', DESCRIPTION: 'Men and Women Clothing'},
        ]

        for cat in categories:
            cursor.execute(
                "INSERT INTO categories (name, description) VALUES (?, ?)",
                (cat[NAME], cat[DESCRIPTION])
            )
        self._connection.commit()

    def _seed_products_data(self, cursor):
        # Retrieve category IDs for mapping
        cursor.execute("SELECT id, name FROM categories")
        cat_mapping = {row[NAME]: row[PRODUCT_ID] for row in cursor.fetchall()}

        # Insert test products
        products = [
            {CATEGORY: 'Electronics', NAME: 'Smartphone', PRICE: 699.99, DESCRIPTION: 'Latest smartphone with advanced features', DISCOUNT: 10.0},
            {CATEGORY: 'Electronics', NAME: 'Laptop', PRICE: 999.99, DESCRIPTION: 'High performance laptop for professionals', DISCOUNT: 15.0},
            {CATEGORY: 'Electronics', NAME: 'Headphones', PRICE: 199.99, DESCRIPTION: 'Noise-cancelling over-ear headphones', DISCOUNT: 5.0},
            {CATEGORY: 'Books', NAME: 'Novel', PRICE: 19.99, DESCRIPTION: 'A captivating fictional story', DISCOUNT: 0.0},
            {CATEGORY: 'Books', NAME: 'Biography', PRICE: 24.99, DESCRIPTION: 'An inspiring life story', DISCOUNT: 0.0},
            {CATEGORY: 'Books', NAME: 'Science Fiction', PRICE: 29.99, DESCRIPTION: 'Futuristic sci-fi adventure', DISCOUNT: 10.0},
            {CATEGORY: 'Clothing', NAME: 'T-Shirt', PRICE: 9.99, DESCRIPTION: 'Comfortable cotton t-shirt', DISCOUNT: 0.0},
            {CATEGORY: 'Clothing', NAME: 'Jeans', PRICE: 49.99, DESCRIPTION: 'Stylish denim jeans', DISCOUNT: 20.0},
            {CATEGORY: 'Clothing', NAME: 'Jacket', PRICE: 79.99, DESCRIPTION: 'Warm and trendy jacket', DISCOUNT: 15.0},
        ]

        for prod in products:
            category_id = cat_mapping.get(prod[CATEGORY])
            if category_id:
                cursor.execute(
                    "INSERT INTO products (category_id, name, price, description, discount) VALUES (?, ?, ?, ?, ?)",
                    (category_id, prod[NAME], prod[PRICE], prod[DESCRIPTION], prod[DISCOUNT])
                )
        self._connection.commit()
