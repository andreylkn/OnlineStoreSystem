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
                    current_user = None
                else:
                    print_invalid_choice()

if __name__ == "__main__":
    main()
