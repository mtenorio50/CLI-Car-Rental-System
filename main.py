from login import LoginSystem
from database import DatabaseConnection
from admin_main import AdminSystem
from staff_main import StaffSystem
from customer_main import CustomerInterface
from termcolor import colored
import os
import msvcrt


def press_any_key():
    print(colored("\nPress any key to continue...", 'yellow', 'on_blue'))
    msvcrt.getch()  # Wait for any key press
    os.system('cls')


def main():
    # Initialize DB and ensure tables exist
    db = DatabaseConnection()
    db.create_tables()
    os.system('cls')

    while True:
        os.system('cls')
        print("\n=== Welcome to Car Rental System ===")
        print("1. Staff/Admin Login")
        print("2. Customer Login")
        print("0. Exit")

        choice = input("\nEnter your choice (0-2): ")

        if choice == '1':
            # Add default admin if not exists
            login_system = LoginSystem()
            user = login_system.login_prompt()
            if user is None:
                continue
            elif user['role'] == 'admin':
                admin_system = AdminSystem()
                admin_system.admin_menu_choice()
            elif user['role'] == 'staff':
                staff_system = StaffSystem()
                staff_system.staff_menu_choice()
            # else:
                # print(colored("Invalid credentials!", "red"))

        elif choice == '2':
            customer = CustomerInterface()
            if customer.login():
                customer.customer_menu()
            else:
                print(colored("Invalid credentials!", "red"))
                press_any_key()

        elif choice == '0':
            print(colored("\nThank you for using our service!", "green"))
            break

        else:
            print(colored("Invalid choice! Please select 0-2", "red"))
            press_any_key()


if __name__ == "__main__":
    main()
