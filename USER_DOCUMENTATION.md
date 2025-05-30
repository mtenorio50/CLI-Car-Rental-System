# Car Rental System - User Documentation

The Car Rental System is a Python-based command-line application designed to manage car rental operations efficiently. It features a role-based access system with three user types: Administrators who manage the entire system, Staff who handle daily rental operations, and Customers who make booking requests. The system provides comprehensive functionality for managing cars, customers, and bookings, including features for adding and tracking vehicles, processing rental requests, managing customer information, and maintaining rental history. Built with SQLite database for data storage, it ensures reliable performance while maintaining data integrity through proper validation and error handling.

## Table of Contents
1. [Getting Started](#getting-started)
2. [User Roles](#user-roles)
3. [Admin Features](#admin-features)
4. [Staff Features](#staff-features)
5. [Customer Features](#customer-features)
6. [Common Operations](#common-operations)
7. [Troubleshooting](#troubleshooting)

## Getting Started

### System Requirements
- Python 3.x installed
- Required Python packages:
  - termcolor
  - prettytable

### Installation
1. Clone the repository
2. Install required packages:
   ```bash
   pip install termcolor
   pip install prettytable
   ```
3. Run the database setup:
   ```bash
   python database.py
   ```
4. Start the application:
   ```bash
   python main.py
   ```

### Default Users
- Admin: username: `admin`, password: `admin`
- Staff: username: `staff`, password: `staff`

## User Roles

### Admin
- Full system access
- Can manage all users, cars, customers, and bookings
- Can approve/reject bookings
- Can view all system reports

### Staff
- Limited system access
- Can view cars and customers
- Can process rentals
- Can view booking requests

### Customer
- Can view available cars
- Can make booking requests
- Can view their booking history
- Can view their rental status

## Admin Features

### User Management
1. View All Users
   - Access: Admin Dashboard → Manage Staff
   - Shows all system users with their details

2. Add User
   - Access: Admin Dashboard → Manage Staff
   - Required fields:
     - Username
     - Password
     - Role (admin/staff)
     - Name
     - Email
     - Phone

3. Edit User
   - Access: Admin Dashboard → Manage Staff
   - Can modify:
     - Password
     - Role (except admin)
     - Email
     - Phone

4. Delete User
   - Access: Admin Dashboard → Manage Staff
   - Cannot delete admin user
   - Requires email confirmation

### Car Management
1. View All Cars
   - Access: Admin Dashboard → Manage Cars
   - Shows all cars with their details

2. Add Car
   - Access: Admin Dashboard → Manage Cars
   - Required fields:
     - Make
     - Model
     - Year
     - Rate per day
     - Registration number

3. Edit Car
   - Access: Admin Dashboard → Manage Cars
   - Can modify rate per day
   - Cannot edit rented cars

4. Delete Car
   - Access: Admin Dashboard → Manage Cars
   - Cannot delete rented cars

### Customer Management
1. View All Customers
   - Access: Admin Dashboard → Manage Customer
   - Shows all customers with their details

2. Add Customer
   - Access: Admin Dashboard → Manage Customer
   - Required fields:
     - Name
     - Phone
     - Email
     - Address
     - License number
     - License expiry date

3. Edit Customer
   - Access: Admin Dashboard → Manage Customer
   - Can modify:
     - Phone
     - Email
     - Address
     - License expiry date

4. Delete Customer
   - Access: Admin Dashboard → Manage Customer
   - Cannot delete customers on rent

### Booking Management
1. View Pending Bookings
   - Access: Admin Dashboard → Manage Bookings
   - Shows all pending booking requests

2. Approve Booking
   - Access: Admin Dashboard → Manage Bookings
   - Steps:
     1. Select booking ID
     2. System validates:
        - Car availability
        - Customer license validity
        - Booking dates
     3. Confirm approval

3. Reject Booking
   - Access: Admin Dashboard → Manage Bookings
   - Steps:
     1. Select booking ID
     2. Enter rejection reason
     3. Confirm rejection

4. View All Bookings
   - Access: Admin Dashboard → Manage Bookings
   - Shows all bookings with their status

## Staff Features

### Car Operations
1. View Available Cars
   - Access: Staff Dashboard → Manage Cars
   - Shows all available cars

2. View Rented Cars
   - Access: Staff Dashboard → Manage Cars
   - Shows all currently rented cars

### Customer Operations
1. View All Customers
   - Access: Staff Dashboard → Manage Customer
   - Shows all customers

2. View Customers on Rent
   - Access: Staff Dashboard → Manage Customer
   - Shows customers with active rentals

### Rental Operations
1. Rent a Car
   - Access: Staff Dashboard → Rent a Car
   - Steps:
     1. Enter customer license number
     2. Select car
     3. Enter rental duration
     4. Confirm rental

2. Return a Car
   - Access: Staff Dashboard → Car Return
   - Steps:
     1. Enter customer license number
     2. Enter car plate number
     3. Add remarks
     4. Confirm return

## Common Operations

### Viewing Rental History
1. Access: Admin/Staff Dashboard → View Rent History
2. Shows all rental records with:
   - Customer details
   - Car details
   - Rental dates
   - Cost
   - Status

### Making a Booking (Customer)
1. Access: Customer Dashboard → Make Booking
2. Steps:
   1. View available cars
   2. Select car
   3. Enter start and end dates
   4. Confirm booking
3. Wait for admin approval

## Troubleshooting

### Common Issues
1. "Booking not found"
   - Check if booking ID is correct
   - Verify booking status is 'pending'

2. "Car not available"
   - Check car status
   - Verify booking dates

3. "Customer already on rent"
   - Check customer's current rental status
   - Process any pending returns

4. "License expired"
   - Check customer's license expiry date
   - Update license information if needed

### Error Messages
- ❌ Red messages indicate errors
- ✅ Green messages indicate success
- ⚠️ Yellow messages indicate warnings

### Getting Help
- Contact system administrator for technical issues
- Check the README.md for system updates
- Review this documentation for common procedures 