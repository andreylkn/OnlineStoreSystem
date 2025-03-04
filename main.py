from models.user.admin import Admin
from models.user.customer import Customer
from services.authorization_service import AuthorizationService
from utils.print_utils import print_guest_menu, print_invalid_choice, print_admin_menu, print_customer_menu


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
        elif type(current_user) is Admin:
            current_user = admin_menu(current_user)
        elif type(current_user) is Customer:
            current_user = customer_menu(current_user)

def admin_menu(user):
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
    elif choice == "10":
        user.print_sales_report()
    elif choice == "11":
        user.export_sales_report()
    elif choice == "12":
        user.show_customer_with_community_discount()
    elif choice == "13":
        user.cancel_community_discount_to_customer()
    elif choice == "0":
        print("Logging out...")
        return None
    else:
        print_invalid_choice()
    return user

def customer_menu(user):
    print_customer_menu()
    choice = input("Choose an option: ").strip()
    if choice == '1':
        user.view_all_categories()  # View Category List
    elif choice == '2':
        user.view_all_products()  # View All Products
    elif choice == '3':
        user.view_products_by_category()  # View Products by Category
    elif choice == '4':
        user.view_cart()   # View Shopping Cart
    elif choice == '5':
        user.add_to_cart()  # Add Product in Cart
    elif choice == '6':
        user.del_prod_in_cart()  # Delete products from the shopping cart
    elif choice == '7':
        user.make_purchase()  # Make a Purchase
    elif choice == "0":
        print("Logging out...")
        return None
    else:
        print_invalid_choice()
    return user

if __name__ == "__main__":
    main()
