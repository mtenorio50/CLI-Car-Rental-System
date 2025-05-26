from database import DatabaseConnection
from datetime import datetime
import msvcrt
from termcolor import colored


def press_any_key2():
    print(colored("\nPress any key to continue...", 'yellow', 'on_blue'))
    msvcrt.getch()  # Wait for any key press


class User:
    def __init__(self):
        self.db = DatabaseConnection()

    def add_user(self, username, password, role):
        try:
            self.db.cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, role)
            )
            self.db.connection.commit()
            print("✅ User added successfully.")
        except Exception as e:
            print("❌ Error adding user:", e)

    def get_all_users(self):
        self.db.cursor.execute("SELECT * FROM users")
        return self.db.cursor.fetchall()


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
        return self.db.cursor.fetchall()

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
        self.db.cursor.execute("SELECT * FROM cars WHERE status = available")
        return self.db.cursor.fetchall()

    def set_availability(self, car_id, is_available):
        try:
            self.db.cursor.execute(
                "UPDATE cars SET is_available = ? WHERE id = ?",
                (is_available, car_id)
            )
            self.db.connection.commit()
        except Exception as e:
            print("❌ Error updating availability:", e)


class Customer:
    def __init__(self):
        self.db = DatabaseConnection()

    def add_customer(self, name, email, phone):
        try:
            self.db.cursor.execute(
                "INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)",
                (name, email, phone)
            )
            self.db.connection.commit()
            print("✅ Customer added successfully.")
        except Exception as e:
            print("❌ Error adding customer:", e)

    def get_all_customers(self):
        self.db.cursor.execute("SELECT * FROM customers")
        return self.db.cursor.fetchall()


class RentLog:
    def __init__(self):
        self.db = DatabaseConnection()

    def log_rental(self, customer_id, car_id):
        try:
            rent_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.cursor.execute(
                "INSERT INTO rent_log (customer_id, car_id, rent_date) VALUES (?, ?, ?)",
                (customer_id, car_id, rent_date)
            )
            self.db.cursor.execute(
                "UPDATE cars SET is_available = 0 WHERE id = ?",
                (car_id,)
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
