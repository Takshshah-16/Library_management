# Library Management System

## Project Overview

This is a comprehensive SQL-based Library Management System implemented with PostgreSQL database and Python CLI interface. The project demonstrates database design, CRUD operations, advanced SQL queries, and stored procedures.

## Project Structure

```
.
├── main.py                         # Main CLI application
├── setup_database.py               # Database initialization script
├── run.sh                          # Startup script
├── start_postgres.sh               # PostgreSQL startup helper
├── books.csv                       # Books data
├── branch.csv                      # Branch data
├── employees.csv                   # Employees data
├── members.csv                     # Members data
├── issued_status.csv               # Issued books data
├── return_status.csv               # Returned books data
├── Library Project advanced.sql    # Advanced SQL queries
└── Library project basic.sql       # Basic SQL queries
```

## Database Schema

The system includes six main tables:

1. **branch**: Library branches with manager and contact information
2. **employees**: Employee records linked to branches
3. **members**: Library member information
4. **books**: Book catalog with ISBN, title, category, rental price, and status
5. **issued_status**: Records of issued books
6. **return_status**: Records of returned books with quality assessment

## Key Features

### 1. Database Operations
- Full CRUD (Create, Read, Update, Delete) operations
- Complex JOIN queries across multiple tables
- Aggregate functions and GROUP BY operations
- Date-based queries for tracking overdue books

### 2. Stored Procedures
- `book_issue`: Manages book issuance and updates availability
- `add_return_records`: Processes book returns and updates status

### 3. CLI Interface Features
- View all books, members, employees, and branches
- Track issued and returned books
- Search books by title, author, or category
- View overdue books (>30 days)
- Generate branch performance reports
- View active members (last 6 months)
- Issue and return books interactively

## Setup and Usage

### Automatic Setup
The system automatically initializes on first run:
1. PostgreSQL database is created and started
2. Tables are created with proper foreign key constraints
3. CSV data is loaded into all tables
4. Stored procedures are created

### Running the Application
Click the "Run" button or execute:
```bash
bash run.sh
```

The CLI menu provides 15 different operations for managing the library system.

## Technical Details

### Database Connection
- PostgreSQL 17
- Unix socket connection (`/tmp/postgresql`)
- Database: `library_db`

### Dependencies
- Python 3.11
- psycopg2-binary (PostgreSQL adapter)
- tabulate (table formatting)
- python-dotenv (environment variables)

## Advanced SQL Features

The project includes implementations of:
- Common Table Expressions (CTEs)
- Window functions for analytics
- Stored procedures with transaction management
- Foreign key constraints and referential integrity
- Date arithmetic for overdue calculations
- Aggregate reporting with multiple JOINs

## Recent Changes

**2025-11-01**: Initial setup in Replit environment
- Configured PostgreSQL database
- Created Python CLI interface
- Set up automated startup workflow
- Loaded sample data from CSV files

## User Preferences

None specified yet.

## Notes

- The database uses Unix socket connections for better performance
- PostgreSQL runs in the background via the workflow system
- The CLI is interactive and menu-driven for ease of use
- Some CSV records with NULL foreign keys are skipped during import
