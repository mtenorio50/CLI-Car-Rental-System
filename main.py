from login import LoginSystem
from database import DatabaseConnection
from admin_main import AdminSystem
from staff_main import StaffSystem
from termcolor import colored


def main():
    # Initialize DB and ensure tables exist
    db = DatabaseConnection()

    # Add default admin if not exists
    login_system = LoginSystem()
    user = None
    while not user:
        user = login_system.login_prompt()

    while True:
        if user['role'] == 'admin':
            admin_system = AdminSystem()
            admin_system.admin_menu_choice()
        elif user['role'] == 'staff':
            staff_system = StaffSystem()
            staff_system.staff_menu_choice()
        else:
            print("Invalid role!")
            break


if __name__ == "__main__":
    main()
