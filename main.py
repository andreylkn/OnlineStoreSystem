from models.user.admin import Admin
from models.user.customer import Customer
from services.authorization_service import AuthorizationService
from utils.print_utils import print_guest_menu, print_invalid_choice, print_admin_menu, print_customer_menu
from models.products.category import Categories
from models.products.product import Products


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
        else:
            validate_admin_cus_role(current_user)

# To verify the role and display the appropriate role function
def validate_admin_cus_role(user):
    if type(user) is Admin:
        print_admin_menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            user.add_category()
        elif choice == "2":
            user.update_category()
        elif choice == "3":
            user.delete_category()
        elif choice == "4":
            user.view_all_categories()
        elif choice == "5":
            user.add_product()
        elif choice == "6":
            user.update_product()
        elif choice == "7":
            user.delete_product()
        elif choice == "8":
            user.view_all_products()
        elif choice == "9":
            user.view_products_by_category()
        elif choice == "0":
            print("Logging out...")
        else:
            print_invalid_choice()
    elif type(user) is Customer:
        print_customer_menu()
        choice = input("Choose an option: ").strip()
        if choice == '1':
            # View Categories List
            view_categ_redirect(user)
        elif choice == '2':
            # View Products
            view_products_redirect(user)
        elif choice == '3':
            # View Shopping Cart
            view_cart_redirect(user)
        else:
            print_invalid_choice()


# View Categories
def view_categ_redirect(user):
    if categories_list := user.view_all_categories():
        selection = int(input("Enter Category ID to view available products, \n\t\t\t\tOR\n"
                              "Enter 0 to return to the Customer Menu: "))
        if selection != 0:
            categories = Categories(categories_list)
            categories.find_selected_category(selection)
            view_selected_categ_prod(user, selection)
        else:
            # 0 Back to the Customer Menu
            validate_admin_cus_role(user)


# View Products
def view_selected_categ_prod(user, selected_category):
    if product_list := user.view_products_from_categ(selected_category):
        selection = int(input("Enter Product ID to to add it to your cart, \n\t\t\t\tOR\n"
                              "Enter 0 to return to the Categories Menu: "))
        if selection != 0:
            quantity = int(input("Enter the quantity: "))
            product = Products(product_list)
            product.find_selected_product(selection)
            user.add_to_cart(selection, quantity)
            view_cart_redirect(user)
        else:
            view_categ_redirect(user)

# View Cart
def view_cart_redirect(user):
    if user.view_cart():
        selected_ID = int(input("Enter the selected Cart ID to remove the product from your cart, \n\t\t\t\tOR\n"
                          "Enter 0 to return to the Categories Menu: "))
        if selected_ID != 0:
            if user.del_prod_in_cart(selected_ID):
                view_cart_redirect(user)
        elif selected_ID == str:
            print_invalid_choice()
        else:
            view_categ_redirect(user)


# View Products
def view_products_redirect(user):
    if product_list := user.view_all_products():
        selection = int(input("Enter Product ID to to add it to your cart, \n\t\t\t\tOR\n"
                              "Enter 0 to return to the Categories Menu: "))
        if selection != 0:
            quantity = int(input("Enter the quantity: "))
            product = Products(product_list)
            product.find_selected_product(selection)
            user.add_to_cart(selection, quantity)
            view_cart_redirect(user)
        else:
            view_categ_redirect(user)

if __name__ == "__main__":
    main()
