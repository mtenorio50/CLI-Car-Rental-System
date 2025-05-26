
from database import DatabaseConnection
import os

import msvcrt
from termcolor import colored


def press_any_key2():
    print(colored("\nPress any key to continue...", 'yellow', 'on_blue'))
    msvcrt.getch()  # Wait for any key press


class LoginSystem:
    def __init__(self):
        self.db = DatabaseConnection()

    def authenticate(self, username, password):
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        self.db.cursor.execute(query, (username, password))
        user = self.db.cursor.fetchone()
        if user:
            print(f"Login successful! Welcome, {user[1]} ({user[3]})")
            press_any_key2()
            return {'id': user[0], 'username': user[1], 'role': user[3]}

        else:
            print("Invalid credentials. Please try again.")
            press_any_key2()
            return None

    def login_prompt(self):
        os.system('cls')
        print("=== Car Rental System Login ===")
        username = input("Username: ")
        password = input("Password: ")  # Hides input
        return self.authenticate(username, password)
