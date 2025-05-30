from database import DatabaseConnection
from datetime import datetime, timedelta
from admin_main import AdminSystem
from utils import Validate
from prettytable import PrettyTable
from termcolor import colored
from models import Car, BookingLog
import os


class CustomerInterface(AdminSystem):
    os.system('cls')

    def __init__(self):
        self.db = DatabaseConnection()
        self.customer_id = None
        self.customer_name = None
        self.license_number = None
        self.car = Car()
        self.booking = BookingLog()
        self.validate = Validate(
            car_instance=self.car, booking_instance=self.booking)

    def login(self):
        os.system('cls')
        print("\n=== Customer Login ===")
        email = input("Enter your email: ")
        license_number = input("Enter your license number: ")

        self.db.cursor.execute('''
            SELECT id, name, license_number FROM customers 
            WHERE email = ? AND license_number = ?
        ''', (email, license_number))

        result = self.db.cursor.fetchone()
        if result:
            self.customer_id, self.customer_name, self.license_number = result
            return True
        return None

    def view_available_cars(self):
        print("\n=== Available Cars ===")
        cars = self.booking.get_available_cars()

        if not cars:
            print(colored("No cars available at the moment.", "yellow"))
            return

        table = PrettyTable()
        table.field_names = ["ID", "Make", "Model",
                             "Year", "Rate/Day", "Plate Number"]
        for car in cars:
            table.add_row(car)
        print(table)
        self.press_any_key2()

    def calculate_rental_cost(self, car_id, start_date, end_date):
        self.db.cursor.execute('''
            SELECT rate_per_day FROM cars WHERE id = ?
        ''', (car_id,))
        rate = self.db.cursor.fetchone()[0]

        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        days = (end - start).days + 1

        return rate * days

    def make_booking(self):
        print("\n=== Make a Booking ===")

        # Check if customer is currently on rent and license validity
        self.db.cursor.execute('''
            SELECT rent_status, license_expiry_date FROM customers 
            WHERE id = ?
        ''', (self.customer_id,))

        result = self.db.cursor.fetchone()
        if not result:
            print(colored("Customer information not found!", "red"))
            self.press_any_key()
            return

        rent_status, license_expiry = result

        # Check if customer is on rent
        if rent_status == 'on rent':
            print(colored(
                "You cannot make a new booking while you have an active rental!", "red"))
            self.press_any_key()
            return

        # Check if license is expired
        license_expiry_date = datetime.strptime(license_expiry, "%Y-%m-%d")
        if license_expiry_date < datetime.now():
            print(colored(
                "Your license has expired! Please renew your license before making a booking.", "red"))
            self.press_any_key()
            return

        # Show available cars
        self.view_available_cars()

        try:
            # Get and validate plate number
            plate_number = self.validate.validate_customer_input(
                "\nEnter plate number of the car you want to book: ", 'plate_number')

            # Get car details
            car_data = self.booking.get_car_details(plate_number)
            if not car_data:
                return

            # Get and validate dates
            start_date = self.validate.validate_customer_input(
                "Start date (YYYY-MM-DD): ", 'start_date')
            end_date = self.validate.validate_customer_input(
                "End date (YYYY-MM-DD): ", 'end_date', start_date)

            # Validate date combination
            # if not self.validate.validate_customer_input([start_date, end_date], 'booking_dates'):
            #    self.press_any_key()
            #    return

            # Check for overlapping bookings
            if not self.booking.check_car_availability(plate_number, start_date, end_date):
                print(
                    colored("❌ Error: This car is already booked for the selected dates!", "red"))
                self.press_any_key()
                return

            # Calculate cost
            total_cost = self.booking.calculate_booking_cost(
                car_data[3], start_date, end_date)
            if total_cost is None:
                self.press_any_key()
                return

            # Create booking request
            if self.booking.create_booking_request(self.license_number, plate_number, start_date, end_date, total_cost):
                print(colored(f"\n✅ Booking request submitted successfully!", "green"))
                print(f"Total cost: ${total_cost}")
                print("Please wait for admin approval.")
            else:
                print(colored("❌ Error: Failed to submit booking request!", "red"))

            self.press_any_key()

        except Exception as e:
            print(colored(f"❌ Error: {str(e)}", "red"))
            self.press_any_key()

    def view_my_bookings(self):
        print("\n=== My Bookings ===")
        bookings = self.booking.get_customer_bookings(self.license_number)

        if not bookings:
            print(colored("You have no bookings.", "yellow"))
            return

        table = PrettyTable()
        table.field_names = ["ID", "License Number", "Plate Number", "Start Date",
                             "End Date", "Cost", "Status", "Remarks"]
        for booking in bookings:
            table.add_row(booking)
        print(table)
        self.press_any_key2()

    def view_active_rent(self):
        print("\n=== My Active Rental ===")
        rental = self.booking.get_active_rental(self.license_number)

        if not rental:
            print(colored("You have no active rentals.", "yellow"))
            self.press_any_key2()
            return

        table = PrettyTable()
        table.field_names = ["Car", "Plate Number",
                             "Rent Date", "Return Date", "Total Cost"]
        table.add_row([
            f"{rental[1]} {rental[2]}",
            rental[0],
            rental[3],
            rental[4],
            f"${rental[5]}"
        ])
        print(table)
        self.press_any_key2()

    def customer_menu(self):
        while True:
            os.system('cls')
            print(f"\n=== Welcome {self.customer_name} ===")
            print("1. View Available Cars")
            print("2. Make a Booking")
            print("3. View My Bookings")
            print("4. View Active Rental")
            print("0. Logout")

            choice = input("\nEnter your choice (0-4): ")

            if choice == '1':
                self.view_available_cars()
            elif choice == '2':
                self.make_booking()
            elif choice == '3':
                self.view_my_bookings()
            elif choice == '4':
                self.view_active_rent()
            elif choice == '0':
                print(colored("\nThank you for using our service!", "green"))
                break
            else:
                print(colored("Invalid choice! Please select 0-4", "red"))
                self.press_any_key()


def main():
    os.system('cls')
    customer = CustomerInterface()
    if not customer.login():
        print(colored("Invalid credentials!", "red"))
        return

    customer.customer_menu()


if __name__ == "__main__":
    main()
