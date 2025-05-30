from database import DatabaseConnection
import os
from admin_main import AdminSystem
import msvcrt
from termcolor import colored
import sys


class LoginSystem(AdminSystem):
    def __init__(self):
        self.db = DatabaseConnection()

    def authenticate(self, username, password):
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        self.db.cursor.execute(query, (username, password))
        user = self.db.cursor.fetchone()
        if user:
            print(f"Login successful! Welcome, {user[1]} ({user[3]})")
            self.press_any_key2()
            return {'id': user[0], 'username': user[1], 'role': user[3]}
        else:
            print(colored("Invalid credentials!", "red"))
            self.press_any_key()
            return None

    def login_prompt(self):
        os.system('cls')
        print("\n=== Car Rental System Login ===")
        username = input("Username: ")
        password = input("Password: ")
        return self.authenticate(username, password)
