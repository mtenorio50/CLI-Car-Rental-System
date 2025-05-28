import sqlite3
import os


class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)

            # Ensure DB is in same directory as main.py
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(base_dir, "car_rental_db.sqlite")

            cls._instance.connection = sqlite3.connect(db_path)
            cls._instance.cursor = cls._instance.connection.cursor()

        return cls._instance

    def create_tables(self):

        # Create users table (admin/staff)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT CHECK(role IN ('admin', 'staff')) NOT NULL,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                phone TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            )
        ''')

        self.cursor.execute('''
            INSERT OR IGNORE INTO users (username, password, role, name, email, phone)
            VALUES ('admin', 'admin', 'admin', 'Admin User', 'admin@example.com', '1234567890'),
                    ('staff', 'staff', 'staff', 'Staff User', 'staff@example.com', '0987654321')
        ''')

        # Create cars table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER CHECK(year > 1900),
                rate_per_day INTEGER NOT NULL CHECK(rate_per_day > 0),
                plate_number TEXT NOT NULL UNIQUE,
                status TEXT DEFAULT 'available',
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            )
        ''')

        # Create customers table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                address TEXT NOT NULL,
                license_number TEXT NOT NULL UNIQUE,
                license_expiry_date TEXT NOT NULL CHECK(
                    license_expiry_date GLOB '????-??-??' AND
                    datetime(license_expiry_date) > datetime('now')
                ),
                rent_status TEXT NOT NULL DEFAULT 'not on rent',
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            )
        ''')

        # Create rent log table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS rent_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                license_number TEXT NOT NULL,
                renter_name TEXT NOT NULL,
                renter_email TEXT NOT NULL,
                plate_number TEXT NOT NULL,
                car_brand TEXT NOT NULL,
                car_model TEXT NOT NULL,             
                rent_date TEXT NOT NULL,
                return_date TEXT,
                total_cost INTEGER,
                status TEXT CHECK(status IN ('rented', 'returned')) DEFAULT 'rented',
                remarks TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            )
        ''')

        self.connection.commit()


# Run this function to create the DB
if __name__ == "__main__":
    db = DatabaseConnection()
    db.create_tables()
    print("Database and tables created successfully.")
