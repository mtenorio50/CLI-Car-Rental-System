from termcolor import colored
from datetime import datetime


class Validate:
    def __init__(self, user_instance=None, car_instance=None, customer_instance=None):
        self.user = user_instance
        self.car = car_instance
        self.customer = customer_instance

    def validate_input(self, prompt, validation_type):

        # prompt (str): The input prompt to show to user
        # validation_type (str): Type of validation to perform
        # user_instance: Instance of User class for database checks

        while True:
            value = input(prompt).strip()

            # Check for blank input
            if not value or value.isspace():
                print(colored("❌ Error: This field cannot be blank", 'red'))
                continue

            # Perform specific validation based on type
            if validation_type == 'username':
                if self.user and self.user.search_user_unique(value):
                    print(
                        colored(f"❌ Error: Username '{value}' already exists!", 'red'))
                    continue
                return value

            elif validation_type == 'email':
                if self.user and self.user.check_useremail_exists(value):
                    print(colored("❌ Error: Email already exists!", 'red'))
                    continue
                return value

            elif validation_type == 'role':
                if value.lower() not in ['admin', 'staff']:
                    print(
                        colored("❌ Error: Role must be either 'admin' or 'staff'", 'red'))
                    continue
                return value.lower()

            elif validation_type == 'phone':
                # No validation for now
                return value

            else:
                return value

    def validate_car_input(self, prompt, validation_type):

        # prompt (str): The input prompt to show to user
        # validation_type (str): Type of validation to perform
        # user_instance: Instance of User class for database checks

        while True:
            value = input(prompt).strip()

            # Check for blank input
            if not value or value.isspace():
                print(colored("❌ Error: This field cannot be blank", 'red'))
                continue

            # Perform specific validation based on type
            if validation_type == 'plate_number':
                # Check if plate number already exists
                if self.car and self.car.search_car_unique(value) is not None:
                    print(
                        colored(f"❌ Error: Plate number '{value}' already exists!", 'red'))
                    continue
                return value.lower()

            elif validation_type == 'rate':
                try:
                    # Convert to float and check if it's positive
                    rate = float(value)
                    if rate <= 0:
                        print(colored("❌ Error: Rate must be greater than 0", 'red'))
                        continue
                    # Format to 2 decimal places
                    return f"{rate:.2f}"
                except ValueError:
                    print(colored("❌ Error: Rate must be a valid number", 'red'))
                    continue

            elif validation_type == 'year':
                try:
                    year = int(value)
                    current_year = datetime.now().year
                    if year < 1900 or year > current_year:
                        print(
                            colored(f"❌ Error: Year must be between 1900 and {current_year}", 'red'))
                        continue
                    return str(year)
                except ValueError:
                    print(colored("❌ Error: Year must be a valid number", 'red'))
                    continue

            elif validation_type == 'general':
                # For make and model - just ensure not empty
                return value

            else:
                return value

    def validate_customer_input(self, prompt, validation_type):

        # prompt (str): The input prompt to show to user
        # validation_type (str): Type of validation to perform
        # user_instance: Instance of User class for database checks

        while True:
            value = input(prompt).strip()

            # Check for blank input
            if not value or value.isspace():
                print(colored("❌ Error: This field cannot be blank", 'red'))
                continue

            # Perform specific validation based on type
            if validation_type == 'license_number':
                # Check if license number already exists
                if self.customer and self.customer.search_customer_unique(value) is not None:
                    print(
                        colored(f"❌ Error: License number '{value}' already exists!", 'red'))
                    continue
                return value.lower()

            elif validation_type == 'email':
                if self.customer and self.customer.check_customeremail_exists(value):
                    print(colored("❌ Error: Email already exists!", 'red'))
                    continue
                return value

            elif validation_type == 'exp_date':
                try:
                    # Try to parse the date
                    expiry_date = datetime.strptime(value, "%Y-%m-%d")
                    current_date = datetime.now()

                    # Check if date is in the future
                    if expiry_date <= current_date:
                        print(
                            colored("❌ Error: Expiry date must be in the future", 'red'))
                        continue

                    return value
                except ValueError:
                    print(colored("❌ Error: Date must be in YYYY-MM-DD format", 'red'))
                    continue

            elif validation_type == 'general':
                # For name, phone, address - just ensure not empty
                return value

            else:
                return value
