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
            self.db.cursor.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            )
            result = self.db.cursor.fetchone()
            if result is None:
                print("❌ User not found with username:", username)
                return None
            return result
        except Exception as e:
            print("❌ Error searching for user:", e)
            return None

    def delete_user(self, username):
        try:
            self.db.cursor.execute(
                "DELETE FROM users WHERE username = ? ", (username,))
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
                SET rate_per_day = ?
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

    def get_available_cars(self):
        self.db.cursor.execute("SELECT * FROM cars WHERE status = 'available'")
        cars = self.db.cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["ID", "Make", "Model", "Year", "Rate/Day",
                             "Plate Number", "Status", "Created At", "Updated At"]
        for car in cars:
            table.add_row(car)
        return table

    def set_availability(self, car_id, is_available):
        try:
            self.db.cursor.execute(
                "UPDATE cars SET is_available = ? WHERE id = ?",
                (is_available, car_id)
            )
            self.db.connection.commit()
        except Exception as e:
            print("❌ Error updating availability:", e)

    def update_car_status(self, plate_number, status):
        try:
            self.db.cursor.execute(
                "UPDATE cars SET status = ? WHERE plate_number = ?",
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
                SET phone = ?, email = ?, address = ?, license_expiry_date = ?
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
            print("❌ Error deleting car:", e)

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
                "UPDATE customers SET rent_status = ? WHERE license_number = ?",
                (rent_status, license_number)
            )
            self.db.connection.commit()
            print("✅ Customer rent status updated successfully.")
            return True
        except Exception as e:
            print("❌ Error updating customer rent status:", e)
            return False


class RentLog:
    def __init__(self):
        self.db = DatabaseConnection()

    def log_rental(self, license_number, plate_number, rent_date, return_date, total_cost):
        try:
            rent_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.cursor.execute(
                "INSERT INTO rent_log (license_number, plate_number, rent_date, return_date, total_cost) VALUES (?, ?, ?, ?, ?)",
                (license_number, plate_number, rent_date, return_date, total_cost)
            )
            self.db.cursor.execute(
                "UPDATE cars SET status = 'rented' WHERE plate_number = ?",
                (plate_number,)
            )
            self.db.connection.commit()
            print("✅ Rental logged successfully.")
        except Exception as e:
            print("❌ Error logging rental:", e)

    def get_rental_history(self):
        self.db.cursor.execute("""
            SELECT r.id, c.name, ca.make || ' ' || ca.model, r.rent_date, r.return_date
            FROM rent_log r
            JOIN customers c ON r.customer_id = c.id
            JOIN cars ca ON r.car_id = ca.id
            ORDER BY r.rent_date DESC
        """)
        return self.db.cursor.fetchall()
