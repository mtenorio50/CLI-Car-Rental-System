# CAR RENTAL SYSTEM

This is a simple Car Rental Management System developed in Python.

## Features

- User authentication (Admin/Staff)
- Car management (Add, Edit Rate, Delete, View)
- Customer management (Add, Edit, Delete, View)
- Booking Management System 
  - Create new bookings
  - View pending bookings
  - Approve/Reject bookings
  - View booking history
- Rent car and log rentals
- View rental history
- Role-based access control (Admin/Staff/Customer permissions)

## Setup

1. Clone the repository.
2. Ensure you have Python installed.
3. Install required libraries:

   ```bash
   pip install termcolor 
   pip install prettytable
   ```
   *(Note: msvcrt is Windows-specific. For other OS, you might need a different library or approach for key press detection.)*
4. Run the `database.py` script to set up the database tables.

     db has default 2 user:
     admin/admin 
     staff/staff

## Running the Application

Run the `main.py` script:

```bash
python main.py
```

Follow the on-screen prompts to login as an admin or staff member and manage the car rental system.

## Version Control

This project is under version control. Commits reflect changes made during development, including bug fixes and feature implementations.

**Last Updated:** 2025-05-30

## Progress

**Update for 2025-05-30:**

- Implemented Booking Management System
  - Added booking creation functionality
  - Implemented booking approval process
  - Added booking rejection with remarks
  - Created booking history view
  - Enhanced booking validation
- Improved Database Operations
  - Added proper transaction handling
  - Enhanced error handling for database operations
  - Improved data consistency checks
- UI/UX Improvements
  - Added emoji indicators for better user feedback
  - Enhanced error messages
  - Improved menu organization

**Update for 2025-05-28:**

- Enhanced Data Management
  - Added timestamp tracking for all records
  - Updated_at field now properly updates on all modifications
  - Improved data integrity with proper timestamp handling
- Improved Customer Management
  - Added validation to prevent deletion of customers on rent
  - Enhanced email validation to prevent duplicates
  - Added proper error handling for customer operations
- Code Improvements
  - Refactored database operations for better consistency
  - Improved error messages and user feedback
  - Enhanced validation logic across all operations
- Staff Page Improvements
  - Completed staff functionality

**Update for 2025-05-27:**

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

**Update for 2024-05-26:**

- Initial Project Setup
  - Created basic project structure
  - Set up database schema
  - Implemented user authentication system
  - Added basic car management features
  - Created initial documentation

