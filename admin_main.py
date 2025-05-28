# from login import LoginSystem
from database import DatabaseConnection
from models import Car, RentLog, Customer, User
from termcolor import colored
from utils import Validate
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
        self.validate = Validate(self.user, self.car, self.customer)

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
                self.return_car()
            elif choice == '6':
                self.rent_history()
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

                username = self.validate.validate_input(
                    "Username: ", 'username')
                password = self.validate.validate_input(
                    "Password: ", 'general')
                role = self.validate.validate_input(
                    "Role - admin or staff: ", 'role')
                name = self.validate.validate_input("Name: ", 'general')
                email = self.validate.validate_input("Email: ", 'email')
                phone = self.validate.validate_input("Phone: ", 'phone')

                if self.user.add_user(username, password, role, name, email, phone):
                    print(colored("✅ User registration completed!", 'green'))
                self.press_any_key()

            elif choice == '3':
                print("\n=== 🧑🏼‍💻 EDIT USER 🧑🏼‍💻 ===")
                username = input("Enter Username to edit: ")
                user_data = self.user.search_user(username)
                if user_data:
                    print("\nLeave blank to keep current value except for role:")
                    new_password = input("New Password: ")
                    if user_data[1] == 'admin':
                        print("⚠️ Warning: Cannot change role of username admin")
                        new_role = 'admin'  # Keep the role as admin
                    else:
                        while True:
                            new_role = input(
                                "New Role - admin or staff: ").lower()
                            if new_role in ['admin', 'staff']:
                                break
                            print(
                                colored("❌ Error: Role must be either 'admin' or 'staff'", 'red'))
                    # Email validation
                    while True:
                        new_email = input("New Email: ").strip()
                        if self.user.check_useremail_exists(new_email):
                            print(colored("❌ Error: Email already exists!", 'red'))
                            continue
                        break
                    new_phone = input("New Phone: ")
                    self.user.edit_user(
                        username, new_password, new_role, new_email, new_phone)
                    self.press_any_key2()
                else:
                    self.press_any_key2()

            elif choice == '4':
                print("\n=== 🧑🏼‍💻 DELETE USER 🧑🏼‍💻 ===")
                while True:
                    username = input("Enter Username to delete: ")
                    if not username or not username.strip():
                        print("❌ Error: Username can not be empty!")
                        self.press_any_key2()
                        break
                    if username == 'admin':
                        print("⚠️ Warning: Can not delete user admin! ")
                        self.press_any_key2()
                        break
                    user_data = self.user.search_user(username)
                    if user_data:
                        print("User", username, "found!")
                        email = input("Enter user email to delete user: ")
                        if not email or not email.strip():
                            print("❌ Error: Email is empty!")
                            self.press_any_key2()
                            break
                        # Email is at index 4 in the users table
                        if email == user_data[5]:
                            self.user.delete_user(username)
                        else:
                            print("❌ Error: Username and Email does not match!")
                            self.press_any_key2()
                            break
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
        6. View Rented Cars
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
                make = self.validate.validate_car_input("Make: ", 'general')
                model = self.validate.validate_car_input("Model: ", 'general')
                year = self.validate.validate_car_input("Year: ", 'year')
                rate_per_day = self.validate.validate_car_input(
                    "Rate/Day: ", 'rate')
                plate_number = self.validate.validate_car_input(
                    "Registration Number: ", 'plate_number')
                status = 'available'
                if self.car.add_car(make, model, year, rate_per_day, plate_number, status):
                    print(colored("Car registration completed!", 'green', 'on_green'))
                self.press_any_key()

            elif choice == '3':
                print("\n=== 🚗 EDIT CAR 🚗 ===")
                plate_number = input("Enter Plate Number to edit: ")
                car_data = self.car.search_car(plate_number)
                if car_data:
                    if car_data[6] == 'rented':  # Check if car status is 'rented'
                        print(
                            "❌ Error: Cannot delete a car that is currently rented!")
                        self.press_any_key2()
                    else:
                        rate_per_day = self.validate.validate_car_input(
                            "Rate/Day: ", 'rate')
                        self.car.edit_car(plate_number, rate_per_day)
                        self.press_any_key2()
                else:
                    self.press_any_key2()

            elif choice == '4':
                print("\n=== 🚗 DELETE CAR 🚗 ===")
                plate_number = input("Enter Car Plate Number to delete: ")
                car_data = self.car.search_car(plate_number)
                if car_data:
                    if car_data[6] == 'rented':  # Check if car status is 'rented'
                        print(
                            "❌ Error: Cannot delete a car that is currently rented!")
                        self.press_any_key2()

                    else:
                        self.car.delete_car(plate_number)
                else:
                    self.press_any_key2()

            elif choice == '0':
                break

            elif choice == '5':
                print("\n=== 🚗 VIEW AVAILABLE CAR/S 🚗 ===")
                cars_table = self.car.get_available_cars()
                print("\n--- All Available Cars ---")
                print(cars_table)
                self.press_any_key()

            elif choice == '6':
                print("\n=== 🚗 VIEW RENTED CAR/S 🚗 ===")
                cars_table = self.car.get_rented_cars()
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
                name = self.validate.validate_customer_input(
                    "Name: ", 'general')
                phone = self.validate.validate_customer_input(
                    "Phone: ", 'general')
                email = self.validate.validate_customer_input(
                    "Email: ", 'email')
                address = self.validate.validate_customer_input(
                    "Address: ", 'general')
                license_number = self.validate.validate_customer_input(
                    "License Number: ", 'license_number').lower()
                license_expiry_date = self.validate.validate_customer_input(
                    "License Exp Date (YYYY-MM-DD): ", 'exp_date')
                rent_status = 'not on rent'

                if self.customer.add_customer(name, phone, email, address, license_number, license_expiry_date, rent_status):
                    print(colored("Customer registration completed!",
                          'green', 'on_green'))
                self.press_any_key()

            elif choice == '3':
                print("\n=== 👨🏻‍💼 EDIT CUSTOMER 👩🏻‍💼 ===")
                license_number = input(
                    "Enter License Number to edit: ").lower()
                customer_data, customer_table = self.customer.search_customer(
                    license_number)
                if customer_data is None:
                    print("❌ Customer not found with license number:",
                          license_number)
                    self.press_any_key2()

                elif customer_data:
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
                    "Enter Customer License Number to delete: ").lower()
                customer_data, customer_table = self.customer.search_customer(
                    license_number)

                if customer_data is None:
                    print("❌ Customer not found with license number:",
                          license_number)
                    self.press_any_key2()
                elif customer_data[7] == 'on rent':  # Check if customer is on rent
                    print(
                        colored("❌ Cannot delete customer who is currently on rent!", 'red'))
                    self.press_any_key2()
                else:
                    print(customer_table)
                    conf = input(
                        "Are you sure you want to delete? Press y to confirm delete: ")

                    if conf in ['y', 'Y']:
                        self.customer.delete_customer(license_number)
                    else:
                        print("Delete Customer cancelled.. ")
                        self.press_any_key2()

            elif choice == '5':
                print("\n=== 👨🏻‍💼 VIEW ALL CUSTOMER ON RENT 👩🏻‍💼 ===")
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
        license_number = input("Enter Customer License Number: ").lower()
        customer_data, customer_table = self.customer.search_customer(
            license_number)

        if customer_data is None:
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

        conf = input("\nConfirm rental? Press y to proceed: ")

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

    def return_car(self):
        print("\n=== 🚗 RETURN A CAR 🚗 ===")
        # Step 1: Get license and plate number
        license_number = input("Enter Customer License Number: ").lower()
        plate_number = input("Enter Rented Plate Number: ").lower()

        renter_result, renter_table = self.rent_log.search_renter(
            license_number, plate_number, status='rented')

        if renter_result is None:
            self.press_any_key2()
            return

        # Display renter information
        print("\nRental Information:")
        print(renter_table)

        remarks = input("Remarks: ")
        conf = input("\nConfirm car return? Press y to confirm return: ")

        if conf.lower() == 'y':
            # Update rental record
            if (self.car.update_car_status(plate_number, 'available') and
                self.customer.update_customer_status(license_number, 'not on rent') and
                    self.rent_log.update_rent_status('returned', remarks, license_number)):
                print("✅ Car return successfully!")
            else:
                print("❌ Failed to process car return!")
        else:
            print("Return cancelled.")

        self.press_any_key2()

    def rent_history(self):
        print("\n=== 🚗 VIEW RENTED CAR/S 🚗 ===")
        rent_table = self.rent_log.get_rental_history()
        print("\n--- Rent History ---")
        print(rent_table)
        self.press_any_key()
