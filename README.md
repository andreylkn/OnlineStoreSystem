# Online Store System

## Description
The Online Store System is a command-line application developed in Python that allows users to browse and purchase everyday goods. The system features distinct roles for administrators and customers, each with specific privileges and functionality. The application is designed with a Command-line User Interface (CUI) to maintain simplicity and ease of use.

## Features
1. **User Management**
   - Registration with optional data-consent for purchase history.
   - Deterministic encryption of user credentials.
   - Role-based access control (Admin vs. Customer).

2. **Product & Category Management**
   - Admin can add, update, and remove categories and products.
   - Customers can browse products by category or view all products.

3. **Community Discounts**
   - Specialized discounts for communities (e.g., students, Māori).
   - Admins can cancel these discounts as needed.

4. **Shopping Cart & Purchases**
   - Customers add items to a cart, review totals (including discounts), and complete purchases.
   - If a user consents, their purchase history is linked to their account.

5. **Sales Reporting**
   - Admin can view or print sales reports by date range.
   - Option to export reports in PDF format using ReportLab.

## Project Structure
```Online Store System
Online Store System
  ├─ managers
  │   ├─ authorization_manager.py
  │   ├─ base_manager.py
  │   ├─ cart_manager.py
  │   ├─ category_manager.py
  │   ├─ community_manager.py
  │   ├─ product_manager.py
  │   ├─ sale_report_manager.py
  ├─ models
  │   └─ user
  │       ├─ admin.py
  │       ├─ customer.py
  │       └─ user.py
  ├─ services
  │   ├─ database.py
  │   └─ deterministic_encryptor.py
  ├─ utils
  │   ├─ input_validation.py
  │   ├─ calculation_utils.py
  │   └─ print_utils.py
  ├─ tests/
  │   ├─ test_auth_manager.py
  │   ├─ test_cart_manager.py
  │   ├─ ...
  ├─ main.py
  ├─ requirements.txt
  ├─ README.md 
  ├─ requirements.txt
  └─ store.db
```

## System Requirements
- **Python**: 3.8 or higher
- **Libraries**:
  - ```sqlite3``` (for database management)
  - ```reportlab``` (for generating PDFs and graphics in Python, install with ```pip install reportlab```)
- **Dependencies**:
  -```pycryptodome``` (provides the AES encryption functionality)
  - ```prettytable``` (for format output, install with ```pip install prettytable```)
  -```pyinstaller```(for building packages for different OS)


## Installation
```bash
# Clone the repository
git clone https://github.com/andreylkn/OnlineStoreSystem.git
cd OnlineStoreSystem

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate # On Windows use: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

## Usage
In the project root (with your virtual environment active), run:
```bash
# Run the application
python main.py
```
You’ll see:
```markdown
========= Online Store System =========
1. Register
2. Login
3. Exit
```

- Register a new account (choose admin or customer).
- Login to begin shopping (as a regular user) or administering the store (if you’re an admin).

If you log in as an administrator, you will see the following menu
```markdown
--------------------- Admin Menu -----------------------
1. Add Category
2. Update Category
3. Delete Category
4. View Categories
5. Add Product
6. Update Product
7. Delete Product
8. View All Products
9. View Products by Category
10. Print Sales Report
11. Export Sales Report to PDF
12. Show Customers with a Community Discount
13. Cancel Community Support Discount for a Customer
0. Logout
```

If you log in as a customer, you will see the customer menu
```markdown
------------------- Customer Menu ----------------------
1. View Category
2. View All Products
3. View Product by Category
4. View Shopping Cart
5. Add Product in Cart
6. Delete Products from the Shopping Cart
7. Make a Purchase
8. Purchase History
0. Logout
```

## Te Tiriti o Waitangi Principles
This project follows the principles of Te Tiriti o Waitangi:
- Partnership: Engages with Māori communities for feedback and support.
- Participation: Offers inclusive discounts for community members (e.g. Māori, students).
- Protection: Safeguards user data (especially Māori data) via encryption, privacy settings, and consent-driven data storage.

## Licensing
**Copyright 2025**

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Online Store System”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


## Contact
- Maintainer: Andrei Kruglov, Ang Lee Ling
- Email: 270411108@yoobeestudent.ac.nz (Andrei Kruglov), 270592687@yoobeestudent.ac.nz (Ang Lee Ling)
- Repo: https://github.com/andreylkn/ClassActivityRepository