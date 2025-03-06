# Online Store System

## Description
The Online Store System is a command-line application developed in Python that allows users to browse and purchase everyday goods. The system features distinct roles for administrators and customers, each with specific privileges and functionality. The application is designed with a Command-line User Interface (CUI) to maintain simplicity and ease of use.

## Features
### Admin Features
- **Category Management**: Add, update, and delete product categories.
- **Product Management**: Add, update, and delete products, including setting discount values.
- **Sales Management**: Print report, export sales report to PDF.
- **View Data**: Display lists of all categories, all products, and products filtered by category.
- **Community Management**: Display customers with a community discount and cancel community support discount for a customer.

### Customer Features
- **Browsing**: View lists of categories, all products, and products by category.
- **Shopping Cart**: Add products to the cart, view cart contents, delete products from the cart.
- **Purchase**: Complete a purchase with price calculation, considering product discounts, and view purchase history.

## Project Structure
```online-store-system/
OnlineStoreSystem/
├── managers/
│   ├── base_manager.py
│   ├── cart_manager.py
│   ├── category_manager.py
│   ├── community_manager.py
│   ├── product_manager.py
│   └── sale_report_manager.py
├── models/
│   └── user/
│       ├── admin.py
│       ├── customer.py
│       └── user.py
├── services/
│   ├── authorization_service.py
│   ├── database.py
│   └── deterministic_encryptor.py
├── utils/
│   ├── calculation_utils.py
│   ├── input_validation.py
│   └── print_utils.py
├── main.py
├── README.md
├── requirements.txt
└── store.db
```

## System Requirements
- **Python**: 3.8 or higher
- **Libraries**:
  - ```sqlite3``` (for database management)
  - ```reportlab``` (for generating PDFs and graphics in Python, install with ```pip install reportlab```)
- **Dependencies**:
  -```bcrypt``` (for cryptographic hashing function designed to securely hash passwords.```pip install bcrypt```)
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
```bash
# Run the application
python main.py
```

## Licensing
**Copyright 2025**

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Car Rental System”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.