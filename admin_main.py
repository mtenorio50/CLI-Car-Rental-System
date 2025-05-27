# from login import LoginSystem
from database import DatabaseConnection
from models import Car, RentLog, Customer, User
from termcolor import colored
import msvcrt
import os
from datetime import datetime, timedelta


class AdminSystem:
    def __init__(self):
        self.db = DatabaseConnection()
        self.car = Car()
        self.customer = Customer()
        self.user = User()
        self.rent_log = RentLog()

    def press_any_key(self):
        print(colored("\nPress any key to continue...", 'yellow', 'on_blue'))
        msvcrt.getch()  # Wait for any key press
        os.system('cls')

    def press_any_key2(self):
        print(colored("\nPress any key to continue...", 'yellow', 'on_blue'))
        msvcrt.getch()  # Wait for any key press

    def show_admin_dashboard(self):
        os.system('cls')
        print("""\n=== Admin Dashboard ===
    1. Manage Staff
    2. Manage Cars
    3. Manage Customer
    4. Rent a Car
    5. Car Return
    6. View Rent History
    0. Logout""")

    def admin_menu_choice(self):
        while True:
            self.show_admin_dashboard()
            choice = input("Enter your choice 0-6: ")
            if choice == '0':
                print(colored("Exiting the program...", 'green', 'on_red'))
                exit()
            elif choice == '1':
                self.staff_management_menu()
            elif choice == '2':
                self.car_management_menu()
            elif choice == '3':
                self.customer_management_menu()
            elif choice == '4':
                self.rent_car()
            elif choice == '5':
                pass
            elif choice == '6':
                pass
            else:
                print(colored("Invalid choice! Select from 0-6", 'green', 'on_red'))
                self.press_any_key()

    def staff_management_menu(self):
        while True:
            os.system('cls')
            print("""\n=== 🧑🏼‍💻 USER MANAGEMENT MENU 👩🏼‍💻===
        1. View All Users
        2. Add User
        3. Edit User
        4. Delete User
        0. Back to Dashboard""")

            choice = input("Choose an option: ")

            if choice == '1':
                print("\n=== 🧑🏼‍💻 VIEW USER/S 🧑🏼‍💻 ===")
                users_table = self.user.get_all_users()
                print("\n--- All User/s ---")
                print(users_table)
                self.press_any_key()

            elif choice == '2':
                print("\n=== 🧑🏼‍💻 ADD USER 🧑🏼‍💻 ===")
                username = input("Username: ")
                password = input("Password: ")
                while True:
                    role = input("Role - admin or staff: ").lower()
                    if role in ['admin', 'staff']:
                        break
                    print(
                        colored("❌ Error: Role must be either 'admin' or 'staff'", 'red'))
                name = input("Name: ")
                email = input("Email: ")
                phone = input("Phone: ")
                if self.user.add_user(username, password, role, name, email, phone):
                    print(colored("User registration completed!", 'green', 'on_green'))
                self.press_any_key()

            elif choice == '3':
                print("\n=== 🧑🏼‍💻 EDIT USER 🧑🏼‍💻 ===")
                username = input("Enter Username to edit: ")
                user_data = self.user.search_user(username)
                if user_data:
                    print("\nLeave blank to keep current value:")
                    new_password = input("New Password: ")
                    while True:
                        new_role = input("New Role - admin or staff: ").lower()
                        if new_role in ['admin', 'staff', ' ']:
                            break
                        print(
                            colored("❌ Error: Role must be either 'admin' or 'staff'", 'red'))
                    new_email = input("New Email: ")
                    new_phone = input("New Phone: ")
                    self.user.edit_user(
                        username, new_password, new_role, new_email, new_phone)
                    self.press_any_key2()
                else:
                    self.press_any_key2()

            elif choice == '4':
                print("\n=== 🧑🏼‍💻 DELETE USER 🧑🏼‍💻 ===")
                username = input("Enter Username to delete: ")
                email = input("Enter User Email: ")
                user_data = self.user.search_user(username, email)
                if user_data:
                    self.user.delete_user(username, email)
                else:
                    self.press_any_key2()

            elif choice == '0':
                break

            else:
                print("❌ Invalid option, select from 1-4, try again.")
                self.press_any_key2()

    def car_management_menu(self):
        while True:
            os.system('cls')
            print("""\n=== 🚗 CAR MANAGEMENT MENU 🚗 ===
        1. View All Cars
        2. Add Car
        3. Edit Car
        4. Delete Car
        5. View Available Cars
        0. Back to Dashboard""")

            choice = input("Choose an option: ")

            if choice == '1':
                print("\n=== 🚗 VIEW CAR/S 🚗 ===")
                cars_table = self.car.get_all_cars()
                print("\n--- All Cars ---")
                print(cars_table)
                self.press_any_key()

            elif choice == '2':
                print("\n=== 🚗 ADD CAR 🚗 ===")
                make = input("Make: ")
                model = input("Model: ")
                year = input("Year: ")
                rate_per_day = input("Rate/Day: ")
                plate_number = input("Registration Number: ").lower()
                status = 'available'
                if self.car.add_car(make, model, year, rate_per_day, plate_number, status):
                    print(colored("Car registration completed!", 'green', 'on_green'))
                self.press_any_key()

            elif choice == '3':
                print("\n=== 🚗 EDIT CAR 🚗 ===")
                plate_number = input("Enter Plate Number to edit: ")
                car_data = self.car.search_car(plate_number)
                if car_data:
                    rate_per_day = input("New Rate Per Day: ")
                    self.car.edit_car(plate_number, rate_per_day)
                    self.press_any_key2()
                else:
                    self.press_any_key2()

            elif choice == '4':
                print("\n=== 🚗 DELETE CAR 🚗 ===")
                plate_number = input("Enter Car Plate Number to delete: ")
                car_data = self.car.search_car(plate_number)
                if car_data:
                    self.car.delete_car(plate_number)
                else:
                    self.press_any_key2()

            elif choice == '0':
                break

            elif choice == '5':
                print("\n=== 🚗 VIEW CAR/S 🚗 ===")
                cars_table = self.car.get_available_cars()
                print("\n--- All Available Cars ---")
                print(cars_table)
                self.press_any_key()

            else:
                print("❌ Invalid option, select from 0-5, try again.")
                self.press_any_key2()

    def customer_management_menu(self):
        while True:
            os.system('cls')
            print("""\n=== 👨🏻‍💼 CUSTOMER MANAGEMENT MENU 👩🏻‍💼 ===
        1. View All Customer
        2. Add Customer
        3. Edit Customer
        4. Delete Customer
        5. On Rent Customer
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
                print("\n=== 👨🏻‍💼 DELETE CUSTOMER 👩🏻‍💼 ===")
                license_number = input(
                    "Enter Customer License Number to delete: ")
                customer_data, customer_table = self.customer.search_customer(
                    license_number)

                if customer_data is None:
                    print("❌ Customer not found with license number:",
                          license_number)
                    self.press_any_key2()
                else:
                    print(customer_table)
                    conf = input(
                        "Are you sure you want to delete? Press y to confirm delete: ")

                    if conf in ['y', 'Y']:
                        self.customer.delete_customer(license_number)
                    else:
                        print("Delete Customer cancelled.. ")

            elif choice == '5':
                print("\n=== 👨��‍💼 VIEW ALL CUSTOMER ON RENT 👩🏻‍💼 ===")
                customers_table = self.customer.get_onrent_customers()
                print("\n--- All Available Cars ---")
                print(customers_table)
                self.press_any_key()

            else:
                print("❌ Invalid option, select from 0-5, try again.")
                self.press_any_key2()

    def rent_car(self):
        print("\n=== 🚗 RENT A CAR 🚗 ===")

        # Step 1: Get customer details
        license_number = input("Enter Customer License Number: ")
        customer_data, customer_table = self.customer.search_customer(
            license_number)

        if customer_data is None:
            print("❌ Customer not found!")
            self.press_any_key2()
            return

        # Check if customer is already renting
        if customer_data[7] == 'on rent':  # rent_status column
            print("❌ Customer already has an active rental!")
            self.press_any_key2()
            return

        # Check if license is valid
        license_expiry = datetime.strptime(
            customer_data[6], "%Y-%m-%d")  # license_expiry_date column
        if license_expiry < datetime.now():
            print("❌ Customer's license has expired!")
            self.press_any_key2()
            return

        # Step 2: Show available cars
        print("\nAvailable Cars:")
        cars_table = self.car.get_available_cars()
        print(cars_table)

        # Step 3: Select car
        plate_number = input("\nEnter Car Plate Number to rent: ").lower()
        car_data = self.car.search_car(plate_number)

        if car_data is None:
            print("❌ Car not found!")
            self.press_any_key2()
            return

        if car_data[6] != 'available':  # status column
            print("❌ Car is not available for rent!")
            self.press_any_key2()
            return

        # Step 4: Get rental duration
        while True:
            try:
                days = int(input("Enter number of days to rent: "))
                if days <= 0:
                    print("❌ Please enter a positive number of days")
                    continue
                break
            except ValueError:
                print("❌ Please enter a valid number")

        # Calculate total cost
        rate_per_day = float(car_data[4])  # rate_per_day column
        total_cost = rate_per_day * days

        # Step 5: Confirm rental
        print(f"\nRental Summary:")
        print(f"Customer: {customer_data[1]}")  # name column
        print(f"Car: {car_data[1]} {car_data[2]}")  # make and model columns
        print(f"Duration: {days} days")
        print(f"Total Cost: ${total_cost:.2f}")

        conf = input("\nConfirm rental? (y/n): ")

        if conf.lower() == 'y':
            # Create rental record
            rent_date = datetime.now().strftime("%Y-%m-%d")
            return_date = (datetime.now() + timedelta(days=days)
                           ).strftime("%Y-%m-%d")

            if self.rent_log.log_rental(license_number, plate_number, rent_date, return_date, total_cost):
                # Update car status
                self.car.update_car_status(plate_number, 'rented')
                # Update customer status
                self.customer.update_customer_status(license_number, 'on rent')
                print("✅ Car rented successfully!")
            else:
                print("❌ Failed to process rental!")
        else:
            print("Rental cancelled.")

        self.press_any_key2()
