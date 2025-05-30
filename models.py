from database import DatabaseConnection
from datetime import datetime
import msvcrt
from termcolor import colored
from prettytable import PrettyTable


def press_any_key2():
    print(colored("\nPress any key to continue...", 'yellow', 'on_blue'))
    msvcrt.getch()  # Wait for any key press


class User:
    def __init__(self):
        self.db = DatabaseConnection()

    def add_user(self, username, password, role, name, email, phone):
        try:
            self.db.cursor.execute(
                "INSERT INTO users (username, password, role, name, email, phone) VALUES (?, ?, ?, ?, ?, ?)",
                (username, password, role, name, email, phone)
            )
            self.db.connection.commit()
            print("✅ User added successfully.")
        except Exception as e:
            print("❌ Error adding user:", e)

    def edit_user(self, username, password, role, email, phone):
        try:
            # First get the current user data
            self.db.cursor.execute(
                "SELECT * FROM users WHERE username = ?", (username,))
            current_user = self.db.cursor.fetchone()

            if current_user is None:
                print("❌ User not found with username:", username)
                return False

            # Keep existing values if new ones are empty
            # username = username if username.strip() else current_user[1]
            password = password if password.strip(
            ) else current_user[2]  # password at index 1
            # role at index 2
            role = role if role.strip() else current_user[3]

            # email at index 3
            email = email if email.strip() else current_user[4]
            # phone at index 4
            phone = phone if phone.strip() else current_user[5]

            self.db.cursor.execute(
                """
                UPDATE users
                SET password = ?, role = ?, email = ?, phone = ?
                WHERE username = ?
                """,
                (password, role, email, phone, username)
            )
            self.db.connection.commit()
            print("✏️ User updated successfully.")
            return True
        except Exception as e:
            print("❌ Error updating user:", e)
            return False

    def search_user(self, username):
        try:
            if not username or not username.strip():
                return None

            self.db.cursor.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,))
            result = self.db.cursor.fetchone()

            if result is None:
                print("❌ User not found with username:", username)
                return None

            return result
        except Exception as e:
            print("❌ Error searching for user:", e)
            return None

    def search_user_unique(self, username):
        try:
            self.db.cursor.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            )
            result = self.db.cursor.fetchone()
            return result
        except Exception as e:
            print("❌ Error searching for user:", e)
            return None

    def check_useremail_exists(self, email):
        try:
            self.db.cursor.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,)
            )
            return self.db.cursor.fetchone() is not None
        except Exception as e:
            print("❌ Error checking email:", e)
            return False

    def delete_user(self, username):
        try:
            self.db.cursor.execute(
                "DELETE FROM users WHERE username = ?", (username,))
            self.db.connection.commit()
            print("🗑️ User deleted successfully.")
            press_any_key2()
        except Exception as e:
            print("❌ Error deleting user:", e)

    def get_all_users(self):
        self.db.cursor.execute("SELECT * FROM users")
        users = self.db.cursor.fetchall()

        # Create a PrettyTable instance
        table = PrettyTable()

        # Add column names matching the database structure
        table.field_names = ["ID", "Username", "Password", "Role",
                             "Name", "Email", "Phone", "Created At", "Updated At"]

        # Add rows
        for user in users:
            table.add_row(user)

        return table


class Car:
    def __init__(self):
        self.db = DatabaseConnection()

    def add_car(self, make, model, year, rate_per_day, plate_number, status):
        try:
            self.db.cursor.execute(
                "INSERT INTO cars (make, model, year, rate_per_day, plate_number, status) VALUES (? ,?, ?, ?, ?, ?)",
                (make, model, year, rate_per_day, plate_number, status)
            )
            self.db.connection.commit()
            print("✅ Car added successfully.")
        except Exception as e:
            print("❌ Error adding car:", e)

    def edit_car(self, plate_number, rate_per_day):
        try:
            self.db.cursor.execute(
                """
                UPDATE cars
                SET rate_per_day = ?, updated_at = datetime('now')
                WHERE plate_number = ?
                """,
                (rate_per_day, plate_number)
            )
            self.db.connection.commit()
            print("✏️ Car rate updated successfully.")
        except Exception as e:
            print("❌ Error updating car rate:", e)

    def delete_car(self, plate_number):
        try:
            self.db.cursor.execute(
                "DELETE FROM cars WHERE plate_number = ?", (plate_number,))
            self.db.connection.commit()
            print("🗑️ Car deleted successfully.")
            press_any_key2()
        except Exception as e:
            print("❌ Error deleting car:", e)

    def get_all_cars(self):
        self.db.cursor.execute("SELECT * FROM cars")
        cars = self.db.cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["ID", "Make", "Model", "Year", "Rate/Day",
                             "Plate Number", "Status", "Created At", "Updated At"]
        for car in cars:
            table.add_row(car)
        return table

    def search_car(self, plate_number):
        try:
            self.db.cursor.execute(
                "SELECT * FROM cars WHERE plate_number = ?",
                (plate_number,)
            )
            result = self.db.cursor.fetchone()
            if result is None:
                print("❌ Car not found with plate number:", plate_number)
                return None
            return result
        except Exception as e:
            print("❌ Error searching for car:", e)
            return None

    def search_car_unique(self, plate_number):
        try:
            self.db.cursor.execute(
                "SELECT * FROM cars WHERE plate_number = ?",
                (plate_number,)
            )
            result = self.db.cursor.fetchone()
            return result
        except Exception as e:
            print("❌ Error searching for car:", e)
            return None

    def get_available_cars(self):
        self.db.cursor.execute("SELECT * FROM cars WHERE status = 'available'")
        cars = self.db.cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["ID", "Make", "Model", "Year", "Rate/Day",
                             "Plate Number", "Status", "Created At", "Updated At"]
        for car in cars:
            table.add_row(car)
        return table

    def get_rented_cars(self):
        self.db.cursor.execute("SELECT * FROM cars WHERE status = 'rented'")
        cars = self.db.cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["ID", "Make", "Model", "Year", "Rate/Day",
                             "Plate Number", "Status", "Created At", "Updated At"]
        for car in cars:
            table.add_row(car)
        return table

    def update_car_status(self, plate_number, status):
        try:
            self.db.cursor.execute(
                "UPDATE cars SET status = ?, updated_at = datetime('now') WHERE plate_number = ?",
                (status, plate_number)
            )
            self.db.connection.commit()
            print("✅ Car status updated successfully.")
            return True
        except Exception as e:
            print("❌ Error updating car status:", e)
            return False


class Customer:
    def __init__(self):
        self.db = DatabaseConnection()

    def add_customer(self, name, phone, email, address, license_number, license_expiry_date, rent_status):
        try:
            self.db.cursor.execute(
                "INSERT INTO customers (name, phone, email, address, license_number, license_expiry_date, rent_status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (name, phone, email, address, license_number,
                 license_expiry_date, rent_status)
            )
            self.db.connection.commit()
            print("✅ Customer added successfully.")
        except Exception as e:
            print("❌ Error adding customer:", e)

    def search_customer(self, license_number):
        try:
            self.db.cursor.execute(
                "SELECT * FROM customers WHERE license_number = ?",
                (license_number,)
            )
            result = self.db.cursor.fetchone()

            if result is None:
                print("❌ Customer not found with license number:", license_number)
                return None, None

            # Create table for display
            table = PrettyTable()
            table.field_names = ["ID", "Name", "Phone", "Email", "Address",
                                 "License Number", "Expiry Date", "Rent Status", "Created At", "Updated At"]
            table.add_row(result)

            return result, table
        except Exception as e:
            print("❌ Error searching for customer:", e)
            return None, None

    def edit_customer(self, license_number, phone, email, address, license_expiry_date):
        try:
            # First get the current user data
            self.db.cursor.execute(
                "SELECT * FROM customers WHERE license_number = ?", (license_number,))
            current_customer = self.db.cursor.fetchone()

            if current_customer is None:
                print("❌ Customer not found with license number:", license_number)
                return False

            # Keep existing values if new ones are empty
            # phone at index 2
            phone = phone if phone.strip() else current_customer[2]
            # email at index 3
            email = email if email.strip() else current_customer[3]
            address = address if address.strip(
            ) else current_customer[4]  # address at index 4
            license_expiry_date = license_expiry_date.strftime(
                "%Y-%m-%d") if license_expiry_date else current_customer[6]  # expiry date at index 6

            self.db.cursor.execute(
                """
                UPDATE customers
                SET phone = ?, email = ?, address = ?, license_expiry_date = ?, updated_at = datetime('now')
                WHERE license_number = ?
                """,
                (phone, email, address, license_expiry_date, license_number)
            )
            self.db.connection.commit()
            print("✏️ Customer updated successfully new information below.")
            return True
        except Exception as e:
            print("❌ Error updating customer:", e)
            return False

    def delete_customer(self, license_number):
        try:
            self.db.cursor.execute(
                "DELETE FROM customers WHERE license_number = ?", (license_number,))
            self.db.connection.commit()
            print("🗑️ Customer deleted successfully.")
            press_any_key2()
        except Exception as e:
            print("❌ Error deleting customer:", e)

    def get_all_customers(self):
        self.db.cursor.execute("SELECT * FROM customers")
        customers = self.db.cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Phone", "Email", "Address",
                             "License Number", "Expiry Date", "Rent Status", "Created At", "Updated At"]
        for customer in customers:
            table.add_row(customer)
        return table

    def get_onrent_customers(self):
        self.db.cursor.execute(
            "SELECT * FROM customers WHERE rent_status = 'on rent'")
        customers = self.db.cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Phone", "Email", "Address",
                             "License Number", "License Expiry Date", "Rent Status", "Created At", "Updated At"]
        for c in customers:
            table.add_row(c)
        return table

    def update_customer_status(self, license_number, rent_status):
        try:
            self.db.cursor.execute(
                "UPDATE customers SET rent_status = ?, updated_at = datetime('now') WHERE license_number = ?",
                (rent_status, license_number)
            )
            self.db.connection.commit()
            print("✅ Customer rent status updated successfully.")
            return True
        except Exception as e:
            print("❌ Error updating customer rent status:", e)
            return False

    def check_customeremail_exists(self, email):
        try:
            self.db.cursor.execute(
                "SELECT * FROM customers WHERE email = ?",
                (email,)
            )
            result = self.db.cursor.fetchone()
            return result

        except Exception as e:
            print("❌ Error checking email:", e)
            return None

    def search_customer_unique(self, license_number):
        try:
            self.db.cursor.execute(
                "SELECT * FROM customers WHERE license_number = ?",
                (license_number,)
            )
            result = self.db.cursor.fetchone()
            return result

        except Exception as e:
            print("❌ Error searching for customer:", e)
            return None


class RentLog:
    def __init__(self):
        self.db = DatabaseConnection()

    def log_rental(self, license_number, plate_number, rent_date, return_date, total_cost):
        try:
            if not rent_date:
                rent_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Get customer name
            self.db.cursor.execute(
                "SELECT name FROM customers WHERE license_number = ?",
                (license_number,)
            )
            customer_result = self.db.cursor.fetchone()
            if not customer_result:
                print("❌ Customer not found!")
                return False
            customer_name = customer_result[0]

            # Get car details
            self.db.cursor.execute(
                "SELECT make, model FROM cars WHERE plate_number = ?",
                (plate_number,)
            )
            car_result = self.db.cursor.fetchone()
            if not car_result:
                print("❌ Car not found!")
                return False
            car_make, car_model = car_result

            # Insert rental record with all details
            self.db.cursor.execute(
                """
                INSERT INTO rent_log 
                (license_number, customer_name, plate_number, car_make, car_model, 
                rent_date, return_date, total_cost, status) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'rented')
                """,
                (license_number, customer_name, plate_number, car_make, car_model,
                 rent_date, return_date, total_cost)
            )

            # Update car status
            self.db.cursor.execute(
                "UPDATE cars SET status = 'rented' WHERE plate_number = ?",
                (plate_number,)
            )
            self.db.connection.commit()
            print("✅ Rental logged successfully.")
            return True
        except Exception as e:
            print("❌ Error logging rental:", e)
            return False

    def search_renter(self, license_number, plate_number, status):
        try:
            self.db.cursor.execute(
                "SELECT * FROM rent_log WHERE license_number = ? AND plate_number = ? AND status = ?",
                (license_number, plate_number, status)
            )
            result = self.db.cursor.fetchone()

            if result is None:
                print("❌ Renter not found with license number and plate number:",
                      license_number, plate_number)
                return None, None

            # Create table for display
            table = PrettyTable()
            table.field_names = ["ID", "License Number", "Plate Number", "Rent Date", "Return Date",
                                 "Total Cost", "Status", "Remarks", "Created At", "Updated At"]
            table.add_row(result)

            return result, table
        except Exception as e:
            print("❌ Error searching for renter:", e)
            return None, None

    def update_rent_status(self, status, remarks, license_number):
        try:
            self.db.cursor.execute(
                "UPDATE rent_log SET status = ?, remarks = ?, updated_at = datetime('now') WHERE license_number = ?",
                (status, remarks, license_number)
            )
            self.db.connection.commit()
            return True
        except Exception as e:
            print("❌ Error updating customer rent status:", e)
            return False

    def get_rental_history(self):
        self.db.cursor.execute("""
            SELECT r.id, c.license_number, c.name, ca.plate_number, ca.make, ca.model, r.rent_date, r.return_date, r.total_cost, r.status, r.remarks
            FROM rent_log r
            JOIN customers c ON r.license_number = c.license_number
            JOIN cars ca ON r.plate_number = ca.plate_number
            ORDER BY r.rent_date DESC
        """)
        rent_table = self.db.cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["ID", "License Number", "Name", "Plate Number", "Car Make", "Car Model",
                             "Rent Date", "Return Date", "Total Cost", "Status", "Remarks"]
        for r in rent_table:
            table.add_row(r)
        return table


class BookingLog:
    def __init__(self):
        self.db = DatabaseConnection()

    def get_available_cars(self):
        """Get all available cars"""
        try:
            self.db.cursor.execute('''
                SELECT id, make, model, year, rate_per_day, plate_number 
                FROM cars 
                WHERE status = 'available'
            ''')
            return self.db.cursor.fetchall()
        except Exception as e:
            print("❌ Error fetching available cars:", e)
            return []

    def get_customer_bookings(self, license_number):
        """Get all bookings for a customer"""
        try:
            self.db.cursor.execute('''
                SELECT br.id, c.make, c.model, br.start_date, br.end_date, 
                       br.total_cost, br.status, br.remarks
                FROM booking_requests br
                JOIN cars c ON br.plate_number = c.plate_number
                WHERE br.license_number = ?
                ORDER BY br.created_at DESC
            ''', (license_number,))
            return self.db.cursor.fetchall()
        except Exception as e:
            print("❌ Error fetching customer bookings:", e)
            return []

    def get_active_rental(self, license_number):
        """Get active rental for a customer"""
        try:
            self.db.cursor.execute('''
                SELECT rl.plate_number, rl.car_make, rl.car_model, 
                       rl.rent_date, rl.return_date, rl.total_cost
                FROM rent_log rl
                WHERE rl.license_number = ? AND rl.status = 'rented'
            ''', (license_number,))
            return self.db.cursor.fetchone()
        except Exception as e:
            print("❌ Error fetching active rental:", e)
            return None

    def check_car_availability(self, plate_number, start_date, end_date):
        # Check if car is available for the given dates
        try:
            self.db.cursor.execute('''
                SELECT COUNT(*) FROM booking_requests 
                WHERE plate_number = ? 
                AND status = 'pending'
                AND (
                    (start_date <= ? AND end_date >= ?) OR
                    (start_date <= ? AND end_date >= ?) OR
                    (start_date >= ? AND end_date <= ?)
                )
            ''', (plate_number, end_date, start_date, start_date, end_date, start_date, end_date))
            return self.db.cursor.fetchone()[0] == 0
        except Exception as e:
            print("❌ Error checking car availability:", e)
            return False

    def get_car_details(self, plate_number):
        """Get car details including rate"""
        try:
            self.db.cursor.execute('''
                SELECT id, make, model, rate_per_day, status 
                FROM cars 
                WHERE plate_number = ?
            ''', (plate_number,))
            return self.db.cursor.fetchone()
        except Exception as e:
            print("❌ Error fetching car details:", e)
            return None

    def calculate_booking_cost(self, rate_per_day, start_date, end_date):
        """Calculate total cost for booking"""
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            days = (end - start).days + 1
            return rate_per_day * days
        except Exception as e:
            print("❌ Error calculating booking cost:", e)
            return None

    def create_booking_request(self, license_number, plate_number, start_date, end_date, total_cost):
        """Create a new booking request"""
        try:
            self.db.cursor.execute('''
                INSERT INTO booking_requests 
                (license_number, plate_number, start_date, end_date, total_cost, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ''', (license_number, plate_number, start_date, end_date, total_cost))

            self.db.connection.commit()
            return True
        except Exception as e:
            print("❌ Error creating booking request:", e)
            return False
