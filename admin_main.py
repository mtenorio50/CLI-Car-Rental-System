# from login import LoginSystem
from database import DatabaseConnection
from models import Car, RentLog, Customer, User
from termcolor import colored
from utils import Validate
from datetime import datetime, timedelta
from prettytable import PrettyTable
import msvcrt
import os
import sqlite3


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
    7. Manage Bookings
    0. Logout""")

    def admin_menu_choice(self):
        while True:
            self.show_admin_dashboard()
            choice = input("Enter your choice 0-7: ")
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
            elif choice == '7':
                self.booking_management_menu()
            else:
                print(colored("Invalid choice! Select from 0-7", 'green', 'on_red'))
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

    def booking_management_menu(self):
        while True:
            os.system('cls')
            print("""\n=== 📋 BOOKING MANAGEMENT MENU 📋 ===
        1. View Pending Bookings
        2. Approve Booking
        3. Reject Booking
        4. View All Bookings
        0. Back to Dashboard""")

            choice = input("Choose an option: ")

            if choice == '1':
                self.view_pending_bookings()
            elif choice == '2':
                self.approve_booking()
            elif choice == '3':
                self.reject_booking()
            elif choice == '4':
                self.view_all_bookings()
            elif choice == '0':
                break
            else:
                print(colored("Invalid choice! Select from 0-4", 'red'))
                self.press_any_key()

    def view_pending_bookings(self):
        print("\n=== 📋 PENDING BOOKINGS 📋 ===")
        self.db.cursor.execute('''
            SELECT * FROM booking_requests WHERE status = 'pending'
        ''')

        bookings = self.db.cursor.fetchall()
        if not bookings:
            print(colored("No pending bookings found.", "yellow"))
            self.press_any_key()
            return

        table = PrettyTable()
        table.field_names = ["ID", "License Number", "Plate Number", "Start Date",
                             "End Date", "Cost", "Status", "Remarks", "Created At", "Updated At"]
        for booking in bookings:
            table.add_row(booking)
        print(table)
        self.press_any_key()

    def approve_booking(self):
        print("\n=== ✅ APPROVE BOOKING ✅ ===")
        print("\n=== ✅PENDING BOOKING LIST ✅ ===")
        self.db.cursor.execute('''
            SELECT * FROM booking_requests WHERE status = 'pending'
        ''')
        bookings = self.db.cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["ID", "License Number", "Plate Number", "Start Date",
                             "End Date", "Cost", "Status", "Remarks", "Created At", "Updated At"]
        for booking in bookings:
            table.add_row(booking)
        print(table)

        if not bookings:
            print(colored("❌ No pending bookings found!", "red"))
            self.press_any_key()
            return

        booking_id = input("Enter booking ID to approve: ")


        try:
            # First check if the booking exists at all
            self.db.cursor.execute('''
                SELECT id, status FROM booking_requests WHERE id = ?
            ''', (booking_id,))

            booking_check = self.db.cursor.fetchone()
            if not booking_check:
                print(
                    colored(f"❌ No booking found with ID: {booking_id}", "red"))
                self.press_any_key()
                return


            # Get booking details with all necessary information
            self.db.cursor.execute('''
                SELECT 
                    br.id,
                    br.license_number,
                    br.plate_number,
                    br.start_date,
                    br.end_date,
                    br.total_cost,
                    br.status,
                    br.remarks,
                    c.name as customer_name,
                    car.make as car_make,
                    car.model as car_model
                FROM booking_requests br
                LEFT JOIN customers c ON br.license_number = c.license_number
                LEFT JOIN cars car ON br.plate_number = car.plate_number
                WHERE br.id = ? AND br.status = 'pending'
            ''', (booking_id,))

            booking = self.db.cursor.fetchone()
            if not booking:
                print(colored("❌ Booking not found or already processed!", "red"))
                self.press_any_key()
                return

            # Extract booking data
            license_number = booking[1]  # license_number
            plate_number = booking[2]    # plate_number
            start_date = booking[3]      # start_date
            end_date = booking[4]        # end_date
            total_cost = booking[5]      # cost
            customer_name = booking[8]   # customer_name from join
            car_make = booking[9]        # car_make from join
            car_model = booking[10]      # car_model from join

            # Update booking status
            self.db.cursor.execute('''
                UPDATE booking_requests 
                SET status = 'approved', updated_at = datetime('now')
                WHERE id = ?
            ''', (booking_id,))

            # Update car status
            self.db.cursor.execute('''
                UPDATE cars 
                SET status = 'rented', updated_at = datetime('now')
                WHERE plate_number = ?
            ''', (plate_number,))

            # Update customer status
            self.db.cursor.execute('''
                UPDATE customers 
                SET rent_status = 'on rent', updated_at = datetime('now')
                WHERE license_number = ?
            ''', (license_number,))

            # Create rent log entry
            self.db.cursor.execute('''
                INSERT INTO rent_log 
                (license_number, customer_name, plate_number, car_make, car_model, 
                rent_date, return_date, total_cost, status) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'rented')
            ''', (license_number, customer_name, plate_number, car_make, car_model,
                  start_date, end_date, total_cost))

            self.db.connection.commit()
            print(colored("✅ Booking approved successfully!", "green"))

        except sqlite3.Error as e:
            print(colored(f"❌ Database error: {str(e)}", "red"))
            self.db.connection.rollback()
        except Exception as e:
            print(colored(f"❌ An error occurred: {str(e)}", "red"))
            self.db.connection.rollback()

        self.press_any_key()

    def reject_booking(self):
        print("\n=== ❌ REJECT BOOKING ❌ ===")
        print("\n=== ❌ PENDING BOOKING LIST❌ ===")
        self.db.cursor.execute('''
            SELECT * FROM booking_requests WHERE status = 'pending'
        ''')
        bookings = self.db.cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["ID", "License Number", "Plate Number", "Start Date",
                             "End Date", "Cost", "Status", "Remarks", "Created At", "Updated At"]
        for booking in bookings:
            table.add_row(booking)
        print(table)
        booking_id = input("Enter booking ID to reject: ")
        remarks = input("Enter rejection reason: ")

        try:
            self.db.cursor.execute('''
                UPDATE booking_requests 
                SET status = 'rejected', remarks = ?, updated_at = datetime('now')
                WHERE id = ? AND status = 'pending'
            ''', (remarks, booking_id))

            if self.db.cursor.rowcount > 0:
                self.db.connection.commit()
                print(colored("Booking rejected successfully!", "green"))
            else:
                print(colored("Booking not found or already processed!", "red"))

        except sqlite3.Error as e:
            print(colored(f"Database error: {str(e)}", "red"))
            self.db.connection.rollback()

        self.press_any_key()

    def view_all_bookings(self):
        print("\n=== 📋 ALL BOOKINGS 📋 ===")
        self.db.cursor.execute('''
            SELECT * FROM booking_requests
        ''')

        bookings = self.db.cursor.fetchall()
        if not bookings:
            print(colored("No bookings found.", "yellow"))
            self.press_any_key()
            return

        table = PrettyTable()
        table.field_names = ["ID", "License Number", "Plate Number", "Start Date",
                             "End Date", "Cost", "Status", "Remarks", "Created At", "Updated At"]
        for booking in bookings:
            table.add_row(booking)
        print(table)
        self.press_any_key()

    def add_booking(self):
        print("\n=== 📋 ADD NEW BOOKING 📋 ===")

        try:
            # Get customer details
            license_number = input("Enter Customer License Number: ").lower()
            customer_data, customer_table = self.customer.search_customer(
                license_number)

            if customer_data is None:
                print(colored("❌ Customer not found!", "red"))
                self.press_any_key()
                return

            # Check if customer is already renting
            if customer_data[7] == 'on rent':  # rent_status column
                print(colored("❌ Customer already has an active rental!", "red"))
                self.press_any_key()
                return

            # Check if license is valid
            license_expiry = datetime.strptime(
                customer_data[6], "%Y-%m-%d")  # license_expiry_date column
            if license_expiry < datetime.now():
                print(colored("❌ Customer's license has expired!", "red"))
                self.press_any_key()
                return

            # Show available cars
            print("\nAvailable Cars:")
            cars_table = self.car.get_available_cars()
            print(cars_table)

            # Get car details
            plate_number = input("\nEnter Car Plate Number: ").lower()
            car_data = self.car.search_car(plate_number)

            if car_data is None:
                print(colored("❌ Car not found!", "red"))
                self.press_any_key()
                return

            if car_data[6] != 'available':  # status column
                print(colored("❌ Car is not available for booking!", "red"))
                self.press_any_key()
                return

            # Get booking dates
            while True:
                try:
                    start_date = input("Enter Start Date (YYYY-MM-DD): ")
                    end_date = input("Enter End Date (YYYY-MM-DD): ")

                    start = datetime.strptime(start_date, "%Y-%m-%d")
                    end = datetime.strptime(end_date, "%Y-%m-%d")

                    if start < datetime.now():
                        print(colored("❌ Start date cannot be in the past!", "red"))
                        continue

                    if end <= start:
                        print(colored("❌ End date must be after start date!", "red"))
                        continue

                    break
                except ValueError:
                    print(colored("❌ Invalid date format! Use YYYY-MM-DD", "red"))

            # Calculate number of days and total cost
            days = (end - start).days
            rate_per_day = float(car_data[4])  # rate_per_day column
            total_cost = rate_per_day * days

            # Show booking summary
            print("\nBooking Summary:")
            print(f"Customer: {customer_data[1]}")  # name column
            # make and model columns
            print(f"Car: {car_data[1]} {car_data[2]}")
            print(f"Start Date: {start_date}")
            print(f"End Date: {end_date}")
            print(f"Duration: {days} days")
            print(f"Total Cost: ${total_cost:.2f}")

            # Confirm booking
            conf = input("\nConfirm booking? Press y to proceed: ")
            if conf.lower() != 'y':
                print("Booking cancelled.")
                self.press_any_key()
                return

            # Create booking record
            self.db.cursor.execute('''
                INSERT INTO booking_requests 
                (license_number, plate_number, start_date, end_date, cost, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, 'pending', datetime('now'), datetime('now'))
            ''', (license_number, plate_number, start_date, end_date, total_cost))

            self.db.connection.commit()
            print(colored("✅ Booking request created successfully!", "green"))

        except sqlite3.Error as e:
            print(colored(f"❌ Database error: {str(e)}", "red"))
            self.db.connection.rollback()
        except Exception as e:
            print(colored(f"❌ An error occurred: {str(e)}", "red"))
            self.db.connection.rollback()

        self.press_any_key()
