from models import Car, RentLog, Customer
from termcolor import colored
import msvcrt
import os
from datetime import datetime, timedelta
from admin_main import AdminSystem


class StaffSystem(AdminSystem):
    def __init__(self):
        super().__init__()

    def show_staff_dashboard(self):
        os.system('cls')
        print("""\n=== Staff Dashboard ===
    1. Manage Cars
    2. Manage Customers
    3. Rent a Car
    4. View Rent History
    0. Logout""")

    def staff_menu_choice(self):
        while True:
            self.show_staff_dashboard()
            choice = input("Enter your choice 0-4: ")
            if choice == '0':
                print(colored("Exiting the program...", 'green', 'on_red'))
                exit()
            elif choice == '1':
                self.car_management_menu()
            elif choice == '2':
                self.customer_management_menu()
            elif choice == '3':
                self.rent_car()
            elif choice == '4':
                pass
            else:
                print(colored("Invalid choice! Select from 0-4", 'green', 'on_red'))
                self.press_any_key()

    def car_management_menu(self):
        while True:
            os.system('cls')
            print("""\n=== 🚗 CAR MANAGEMENT MENU 🚗 ===
        1. View All Cars
        2. View Available Cars
        0. Back to Dashboard""")

            choice = input("Choose an option: ")

            if choice == '1':
                print("\n=== 🚗 VIEW CAR/S 🚗 ===")
                cars_table = self.car.get_all_cars()
                print("\n--- All Cars ---")
                print(cars_table)
                self.press_any_key()

            elif choice == '2':
                print("\n=== 🚗 VIEW CAR/S 🚗 ===")
                cars_table = self.car.get_available_cars()
                print("\n--- All Available Cars ---")
                print(cars_table)
                self.press_any_key()

            elif choice == '0':
                break

            else:
                print("❌ Invalid option, select from 0-2, try again.")
                self.press_any_key2()

    def customer_management_menu(self):
        while True:
            os.system('cls')
            print("""\n=== 👨🏻‍💼 CUSTOMER MANAGEMENT MENU 👩🏻‍💼 ===
            1. View All Customer
            2. Add Customer
            3. Edit Customer
            4. On Rent Customer
            0. Back to Dashboard""")

            choice = input("Choose an option: ")

            if choice == '0':
                break

            elif choice == '1':
                print("\n=== 👨🏻‍💼 VIEW CUSTOMER/S 👩🏻‍💼 ===")
                customer_table = self.customer.get_all_customers()
                print("\n--- All Customers ---")
                print(customer_table)
                self.press_any_key()

            elif choice == '2':
                print("\n=== 👨🏻‍💼 ADD CUSTOMER 👩🏻‍💼 ===")
                name = input("Name: ")
                phone = input("Phone: ")
                email = input("Email: ")
                address = input("Address: ")
                license_number = input("License Number: ")

                while True:
                    try:
                        date_str = input("License Exp Date (YYYY-MM-DD): ")
                        license_expiry_date = datetime.strptime(
                            date_str, "%Y-%m-%d")
                        if license_expiry_date < datetime.now():
                            print(
                                colored("❌ Error: License expiry date must be in the future", 'red'))
                            continue
                        break
                    except ValueError:
                        print(
                            colored("❌ Error: Please enter date in YYYY-MM-DD format", 'red'))

                rent_status = 'not on rent'
                if self.customer.add_customer(name, phone, email, address, license_number, license_expiry_date.strftime("%Y-%m-%d"), rent_status):
                    print(colored("Customer registration completed!",
                          'green', 'on_green'))
                self.press_any_key()

            elif choice == '3':
                print("\n=== 👨🏻‍💼 EDIT CUSTOMER 👩🏻‍💼 ===")
                license_number = input("Enter License Number to edit: ")
                customer_data, customer_table = self.customer.search_customer(
                    license_number)
                if customer_data:
                    print("Customer found: ")
                    print(customer_table)
                    print(
                        "\nLeave blank to keep current value except license expiry date:")
                    new_phone = input("New Phone: ")
                    new_email = input("New Email: ")
                    new_address = input("New Address: ")

                    while True:
                        try:
                            date_str = input(
                                "New License Expiry Date (YYYY-MM-DD): ")
                            new_license_expiry_date = datetime.strptime(
                                date_str, "%Y-%m-%d")
                            if new_license_expiry_date < datetime.now():
                                print(
                                    colored("❌ Error: License expiry date must be in the future", 'red'))
                                continue
                            break
                        except ValueError:
                            print(
                                colored("❌ Error: Please enter date in YYYY-MM-DD format", 'red'))

                    self.customer.edit_customer(
                        license_number, new_phone, new_email, new_address, new_license_expiry_date)
                    customer_data, customer_table = self.customer.search_customer(
                        license_number)
                    print(customer_table)
                    self.press_any_key2()

            elif choice == '4':
                print("\n=== 👨🏻‍💼 VIEW ALL CUSTOMER ON RENT 👩🏻‍💼 ===")
                customers_table = self.customer.get_onrent_customers()
                print("\n--- All Available Cars ---")
                print(customers_table)
                self.press_any_key()

            else:
                print("❌ Invalid option, select from 0-4, try again.")
                self.press_any_key2()
