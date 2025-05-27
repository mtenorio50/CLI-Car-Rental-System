# CAR RENTAL SYSTEM

This is a simple Car Rental Management System developed in Python.

## Features

- User authentication (Admin/Staff)
- Car management (Add, Edit Rate, Delete, View)
- Customer management (Add, Edit, Delete, View)
- Rent car and log rentals
- View rental history
- Role-based access control (Admin/Staff permissions)

## Setup

1. Clone the repository.
2. Ensure you have Python installed.
3. Install required libraries:

   ```bash
   pip install termcolor prettytable
   ```
   *(Note: msvcrt is Windows-specific. For other OS, you might need a different library or approach for key press detection.)*
4. Run the `database.py` script to set up the database tables.

## Running the Application

Run the `main.py` script:

```bash
python main.py
```

Follow the on-screen prompts to login as an admin or staff member and manage the car rental system.

## Version Control

This project is under version control. Commits reflect changes made during development, including bug fixes and feature implementations.

**Last Updated:** 2024-05-27

## Progress

- Implemented user authentication (Admin/Staff).
- Implemented basic car management (Add, Edit Rate, Delete, View).
- Added car search by plate number with error handling.
- Adjusted car editing to focus on rate per day.
- Setup basic database structure.
- Created initial README file.
- Updated delete car functionality to use plate number.

**Next Steps:**

- Implement Customer Management.
- Implement Renting a Car.
- Implement Viewing Rent History.
- Refine user interface and add input validation.
- Consider cross-platform compatibility for msvcrt.

**Latest Updates (2024-05-27):**

- Implemented Customer Management
  - Add new customers
  - Edit customer details
  - Delete customers
  - View all customers
  - View customers on rent
- Implemented Renting a Car
  - License validation
  - Car availability check
  - Rental duration and cost calculation
  - Status updates for cars and customers
- Implemented role-based access control
  - Admin: Full access to all features
  - Staff: Limited access to certain features

**Next Steps:**

- Implement Car Return functionality
- Implement Viewing Rent History
- Add data validation and error handling improvements
- Add unit tests
- Consider cross-platform compatibility for msvcrt
- Add data export functionality
- Implement reporting features