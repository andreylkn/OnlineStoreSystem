from models.user.admin import Admin
from models.user.customer import Customer
from services.authorization_service import AuthorizationService
from utils.print_utils import print_guest_menu, print_invalid_choice, print_admin_menu, print_customer_menu
from models.features.customer_function import CustomerFeatures
from models.products.category import Categories
from models.products.product import Products

cust_features = CustomerFeatures()


def main():
    auth_service = AuthorizationService()
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

            validate_admin_cus_role(current_user)


def validate_admin_cus_role(user):
    # To verify the role and display the appropriate role function
    if type(user) is Admin:
        print_admin_menu()
        choice = input("Choose an option: ").strip()
        if choice == '1':
            print("Will be available soon.")
        else:
            print_invalid_choice()
    elif type(user) is Customer:
        print_customer_menu()
        choice = input("Choose an option: ").strip()
        if choice == '1':
            # View Categories List
            redirect_to_view_categories(user)
        if choice == '2':
            # View Shopping Cart
            redirect_to_view_cart(user)
        else:
            print_invalid_choice()


def redirect_to_view_categories(user):
    # View Categories
    if categories_list := cust_features.view_categories():

        selection = int(input("Enter Category ID to view available products, \n\t\t\t\tOR\n"
                              "Enter 0 to return to the Customer Menu: "))

        if selection != 0:
            categories = Categories(categories_list)
            categories.find_selected_category(selection)
            redirect_to_view_products(user, selection)
        else:
            # 0 Back to the Customer Menu
            validate_admin_cus_role(user)


def redirect_to_view_products(user, selected_category):
    # View Products
    if product_list := cust_features.view_products(selected_category):

        selection = int(input("Enter Product ID to to add it to your cart, \n\t\t\t\tOR\n"
                              "Enter 0 to return to the Categories Menu: "))

        if selection != 0:
            quantity = int(input("Enter the quantity: "))
            product = Products(product_list)
            product.find_selected_product(selection)
            cust_features.add_to_cart(selection, quantity)
            redirect_to_view_cart(user)

        else:
            redirect_to_view_categories(user)


def redirect_to_view_cart(user):
    if cust_features.view_cart(Customer._current_user_id):
        selected_ID = int(input("Enter the selected Cart ID to remove the product from your cart, \n\t\t\t\tOR\n"
                          "Enter 0 to return to the Categories Menu: "))

        if selected_ID != 0:
            cust_features.delete_product_in_cart(selected_ID)
        elif selected_ID == str:
            print_invalid_choice()
        else:
            redirect_to_view_categories(user)


if __name__ == "__main__":
    main()
