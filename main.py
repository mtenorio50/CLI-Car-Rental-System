from login import LoginSystem
from database import DatabaseConnection
from models import Car, RentLog, Customer
from termcolor import colored
import msvcrt
import os


def press_any_key():
    print(colored("\nPress any key to continue...", 'yellow', 'on_blue'))
    msvcrt.getch()  # Wait for any key press
    os.system('cls')


def press_any_key2():
    print(colored("\nPress any key to continue...", 'yellow', 'on_blue'))
    msvcrt.getch()  # Wait for any key press


def show_admin_dashboard():
    os.system('cls')
    print("""\n=== Admin Dashboard ===
    1. Manage Staff
    2. Manage Cars
    3. Manage Customer
    4. Rent a Car
    5. View Rent History
    0. Logout""")


def admin_menu_choice():
    while True:
        show_admin_dashboard()
        choice = input("Enter your choice 0-5: ")
        if choice == '0':
            print(colored("Exiting the program...", 'green', 'on_red'))
            exit()
        elif choice == '1':
            print(colored("Register Staff", 'green', 'on_blue'))
            user = User()
            user.set_user(
                input("Enter username: "),
                input("Enter password: "),
                input("Enter full name: "),
                input("Enter email: "),
                input("Enter phone number: "),
                input("Enter role (admin/staff): ")
            )
            if add_user(**user.get_user()):
                print(colored("Staff registration completed!", 'green', 'on_green'))
            press_any_key()

        elif choice == '2':
            car_management_menu()

        elif choice == '3':
            pass

        elif choice == '4':
            pass

        else:
            print(colored("Invalid choice! Select from 0-5", 'green', 'on_red'))
            press_any_key()


def car_management_menu():
    car = Car()

    while True:
        os.system('cls')
        print("""\n=== 🚗 CAR MANAGEMENT MENU ===
        1. View All Cars
        2. Add Car
        3. Edit Car
        4. Delete Car
        5. Rent a Car
        6. Back to Dashboard""")

        choice = input("Choose an option: ")

        if choice == '1':
            print("\n=== 🚗 VIEW CAR/S ===")
            cars = car.get_all_cars()
            print("\n--- All Cars ---")
            for c in cars:
                print(list(c))
            press_any_key()

        elif choice == '2':
            print("\n=== 🚗 ADD CAR ===")
            make = input("Make: ")
            model = input("Model: ")
            year = input("Year: ")
            rate_per_day = input("Rate/Day: ")
            plate_number = input("Registration Number: ").lower()
            status = 'available'
            if car.add_car(make, model, year, rate_per_day, plate_number, status):
                print(colored("Car registration completed!", 'green', 'on_green'))
            press_any_key()

        elif choice == '3':
            plate_number = input("Enter Plate Number to edit: ")
            car_data = car.search_car(plate_number)
            if car_data:
                rate_per_day = input("New Rate Per Day: ")
                car.edit_car(plate_number, rate_per_day)
            else:
                press_any_key2()

        elif choice == '4':
            plate_number = input("Enter Car Plate Number to delete: ")
            car_data = car.search_car(plate_number)
            if car_data:
                car.delete_car(plate_number)
            else:
                press_any_key2()

        elif choice == '5':
            customer = Customer()
            customers = customer.get_all_customers()
            print("\n--- Customers ---")
            for c in customers:
                print(f"{c[0]}. {c[1]} ({c[2]}, {c[3]})")

            customer_id = input("Enter Customer ID: ")

            available_cars = car.get_available_cars()
            print("\n--- Available Cars ---")
            for c in available_cars:
                print(f"{c[0]}. {c[1]} {c[2]} ({c[3]}) | Reg: {c[4]}")

            car_id = input("Enter Car ID to rent: ")

            RentLog().log_rental(customer_id, car_id)

        elif choice == '6':
            break

        else:
            print("❌ Invalid option, select from 1-6, try again.")
            press_any_key2()


def show_staff_dashboard():
    print("""\n=== Staff Dashboard ===
    1. Manage Cars
    2. Manage Customers
    3. Rent a Car
    4. View Rent History
    0. Logout""")


def main():
    # Initialize DB and ensure tables exist
    db = DatabaseConnection()

    # Add default admin if not exists
    login_system = LoginSystem()
    user = None
    while not user:
        user = login_system.login_prompt()

    while True:
        if user['role'] == 'admin':
            admin_menu_choice()
        elif user['role'] == 'staff':
            show_staff_dashboard()

        choice = input("Select an option: ")
        if choice == "0":
            print("👋 Logging out...")
            break
        else:
            print("⚙️ Functionality coming soon...")


if __name__ == "__main__":
    main()
