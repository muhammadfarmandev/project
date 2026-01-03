# NSOS - National Security Operation System

A simple web-based police station management system built for learning purposes. This project demonstrates Object-Oriented Programming concepts, database CRUD operations, and basic web development.

## Project Overview

NSOS is a basic police station management system that helps manage:
- Officers and their assignments
- Criminal records
- FIR/Case management
- Evidence tracking
- Duty assignments
- Case updates and proceedings

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Backend**: Python Flask
- **Database**: Microsoft SQL Server
- **Database Library**: pyodbc
- **Password Hashing**: bcrypt

## Features

### 1. Admin Login
- Simple username/password authentication
- Session-based authentication
- Password stored as hashed value

### 2. Officer Management (CRUD)
- Add new officers
- View all officers
- Update officer information
- Delete officers
- Assign officers to units

### 3. Criminal Management (CRUD)
- Add criminal records
- View all criminals
- Update criminal information
- Delete criminal records

### 4. FIR/Case Management
- Register new cases (FIRs)
- View all cases
- Update case status (Open/Closed)
- Link cases to officers and suspects
- Delete cases

### 5. Case Updates
- Add progress notes to cases
- View case history
- Track case proceedings

### 6. Evidence Management
- Upload evidence files (PDF, images, documents)
- Add descriptions to evidence
- Link evidence to cases
- Download evidence files

### 7. Duty Assignment
- Assign duties to officers
- View duty schedule
- Delete duty assignments

### 8. Search Functionality
- Search cases by case number or officer name
- Search criminals by name or CNIC

### 9. Audit Log
- Automatic logging of all CRUD operations
- Track actions, table names, and timestamps

## OOP Concepts Demonstrated

### 1. Inheritance
- `Person` base class
- `Officer` and `Criminal` inherit from `Person`

### 2. Encapsulation
- Private attributes using `_` prefix
- Getter and setter methods

### 3. Abstraction
- Abstract method `get_info()` in `Person` class
- Subclasses must implement this method

### 4. Polymorphism
- Different implementations of `get_info()` in `Officer` and `Criminal` classes

### 5. Constructors
- `__init__` methods in all classes
- Proper initialization of attributes

## Database Schema

### Tables

1. **Admin** - Admin credentials
2. **Unit** - Police units (Investigation, Patrol, Admin)
3. **Officer** - Officer details
4. **Criminal** - Criminal records
5. **Case** - FIR/Case records
6. **CaseUpdate** - Case progress notes
7. **Evidence** - Evidence records
8. **Duty** - Duty assignments
9. **AuditLog** - Action logs

### Relationships

- Officer → Unit (many-to-one)
- Case → Officer (filed_by)
- Case → Criminal (suspect_id)
- CaseUpdate → Case (many-to-one)
- CaseUpdate → Officer (updated_by)
- Evidence → Case (many-to-one)
- Duty → Officer (many-to-one)

## Setup Instructions

### Prerequisites

1. Python 3.7 or higher
2. Microsoft SQL Server
3. ODBC Driver for SQL Server

### Installation Steps

1. **Clone or download the project**

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up SQL Server Database**
   - Open SQL Server Management Studio
   - Create a new database named "NSOS"
   - Run the SQL script from `database/schema.sql` to create tables and insert sample data

4. **Configure Database Connection**
   - Edit `backend/config.py`
   - Update `DB_SERVER` if your SQL Server is not on localhost
   - Update `DB_NAME` if you used a different database name
   - Update `DB_DRIVER` to match your ODBC driver version

5. **Set Admin Password**
   - The default admin credentials are: username: `admin`, password: `admin123`
   - To set a new password, you can use Python:
     ```python
     import bcrypt
     password = "your_password"
     hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
     print(hashed.decode('utf-8'))
     ```
   - Update the `password_hash` in the Admin table with the generated hash

6. **Run the Application**
   ```bash
   cd backend
   python app.py
   ```

7. **Access the Application**
   - Open browser and go to: `http://localhost:5000`
   - Login with admin credentials

## Project Structure

```
project/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── config.py           # Database configuration
│   ├── models.py           # OOP classes
│   ├── database.py         # Database CRUD operations
│   ├── routes.py           # Flask routes
│   └── utils.py            # Helper functions
├── frontend/
│   ├── index.html          # Login page
│   ├── dashboard.html      # Dashboard
│   ├── officers.html       # Officer management
│   ├── criminals.html      # Criminal management
│   ├── cases.html          # Case management
│   ├── case-details.html   # Case details
│   ├── evidence.html       # Evidence management
│   ├── duties.html         # Duty assignment
│   ├── search.html         # Search
│   ├── css/
│   │   └── style.css       # Stylesheet
│   └── js/
│       ├── api.js          # API calls
│       ├── auth.js         # Authentication
│       └── *.js            # Page-specific scripts
├── uploads/                # Evidence file storage
├── database/
│   └── schema.sql          # Database schema
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

## ER Diagram

```
┌─────────┐      ┌─────────┐
│  Admin  │      │  Unit   │
└─────────┘      └────┬────┘
                     │
                     │ 1
                     │
                ┌────┴────┐
                │ Officer │
                └────┬────┘
                     │ 1
                     │
                ┌────┴────┐
                │  Case   │
                └────┬────┘
                     │ 1
         ┌───────────┼───────────┐
         │          │           │
    ┌────┴────┐ ┌───┴────┐ ┌────┴────┐
    │Criminal│ │CaseUpdt│ │Evidence │
    └────────┘ └────────┘ └─────────┘
                     │
                ┌────┴────┐
                │  Duty  │
                └────────┘
```

## UML Class Diagram

```
┌─────────────────┐
│     Person      │ (Abstract)
├─────────────────┤
│ - _name         │
│ - _address      │
├─────────────────┤
│ + get_name()    │
│ + get_address() │
│ + get_info()    │ (Abstract)
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───┴───┐ ┌──┴──────┐
│Officer│ │Criminal│
├───────┤ ├────────┤
│_badge │ │_cnic   │
│_rank  │ │_notes  │
│_contact│ │        │
│_unit_id│ │        │
├───────┤ ├────────┤
│get_info│ │get_info│
└───────┘ └────────┘
```

## Screenshots

(Add screenshots of the working system here)

## Notes

- This project is designed for educational purposes
- It demonstrates basic OOP concepts and CRUD operations
- The code is intentionally kept simple to match a 2nd-semester student level
- Some naming conventions may be inconsistent (intentional for learning purposes)

## Default Credentials

- Username: `admin`
- Password: `admin123`

**Important**: Change the default password in production!

## License

This project is for educational purposes only.

## Author

2nd Semester Computer Science Student Project

