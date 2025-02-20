from models.user.admin import Admin
from models.user.customer import Customer
from services.authorization_service import AuthorizationService
from utils.print_utils import print_guest_menu, print_invalid_choice, print_admin_menu, print_customer_menu
from models.features.customer_function import CustomerFeatures
from models.products.category import Categories
from models.products.product import Products

def main():
    auth_service = AuthorizationService()
    cust_features = CustomerFeatures()

    current_user = None

    while True:
        if current_user is None:
            print_guest_menu()
            choice = input("Choose an option: ").strip()
            if choice == '1':
                auth_service.register_user()
            elif choice == '2':
                current_user = auth_service.authenticate()
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print_invalid_choice()
            if type(current_user) is Admin:
                print_admin_menu()
                choice = input("Choose an option: ").strip()
                if choice == '1':
                    current_user = None
                else:
                    print_invalid_choice()
            elif type(current_user) is Customer:
                print_customer_menu()
                choice = input("Choose an option: ").strip()
                if choice == '1':
                    if categories_list := cust_features.view_categories():
                        # 20/2 implement press 0 to go back Customer Menu
                        selected_category = int(input("Choose a category from the table above to see available "
                                                      "products: "))
                        categories = Categories(categories_list)
                        categories.find_selected_category(selected_category)

                        # Option to make a purchase or back to Customer Menu
                        if product_list := cust_features.view_products(selected_category):
                            selected_product = int(input("Enter the product ID to add it to your cart: "))
                            quantity = int(input("Enter the quantity: "))
                            product = Products(product_list)
                            product.find_selected_product(selected_product)
                            cust_features.add_to_cart(selected_product, quantity)
                            cust_features.view_cart(Customer._current_user_id)
                    break
                if choice == '2':
                    # View Shopping Cart
                    cust_features.view_cart(Customer._current_user_id)
                else:
                    print_invalid_choice()


if __name__ == "__main__":
    main()
