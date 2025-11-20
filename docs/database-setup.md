# Database Setup and Documentation

## Overview

The ABC Payroll System uses SQLite as its database backend. The database stores employee information, compensation details, user accounts, time entries, and payroll records.

## Database Structure

### Core Tables

#### `employees`

Stores employee demographic and employment information.

**Key Fields:**

- `employee_id` (TEXT, Primary Key) - Unique employee identifier (e.g., E001)
- `first_name`, `last_name`, `surname` - Employee name fields
- `date_of_birth` (TEXT) - Must be 18+ years old
- `gender` (TEXT) - Male or Female
- `email` (TEXT, Unique) - Company email address
- `address_line1`, `address_line2`, `city`, `state`, `zip_code` - Address fields
- `status` (TEXT) - Active or Terminated
- `date_hired` (TEXT) - Employment start date
- `has_picture` (INTEGER) - Boolean flag for profile picture
- `picture_filename` (TEXT) - Path to employee picture
- `department_id` (INTEGER, Foreign Key) - Links to departments table
- `job_title_id` (INTEGER, Foreign Key) - Links to job_titles table

**Constraints:**

- Age validation: Employee must be at least 18 years old
- Unique email addresses
- Status must be 'Active' or 'Terminated'

#### `departments`

Stores organizational departments.

**Fields:**

- `department_id` (INTEGER, Primary Key, Autoincrement)
- `department_name` (TEXT, Unique) - Department name

#### `job_titles`

Stores job title information.

**Fields:**

- `job_title_id` (INTEGER, Primary Key, Autoincrement)
- `title_name` (TEXT, Unique) - Job title

#### `compensation`

Stores employee compensation and benefits information.

**Key Fields:**

- `compensation_id` (INTEGER, Primary Key, Autoincrement)
- `employee_id` (TEXT, Foreign Key) - Links to employees table
- `salary_type` (TEXT) - 'Salary' or 'Hourly'
- `base_salary` (REAL) - Annual salary (for salaried employees)
- `hourly_rate` (REAL) - Hourly pay rate (for hourly employees)
- `medical_type` (TEXT) - 'Single' or 'Family'
- `num_dependents` (INTEGER) - Number of dependents (for stipend calculation)
- `effective_date` (TEXT) - When compensation takes effect

**Business Rules:**

- Medical coverage: $50 (Single) or $100 (Family) per pay period
- Dependent stipend: $45 per dependent

#### `users`

Stores authentication credentials and user types.

**Key Fields:**

- `user_id` (INTEGER, Primary Key, Autoincrement)
- `username` (TEXT, Unique) - Login username
- `password_hash` (TEXT) - SHA256 hashed password
- `user_type` (TEXT) - 'Admin' or 'Employee'
- `employee_id` (TEXT, Foreign Key, Optional) - Links to employees table for employee users
- `is_active` (INTEGER) - Account status (1 = active, 0 = disabled)
- `last_login` (TEXT) - Last successful login timestamp

**Default Accounts:**

- Admin: Username `HR0001`, Password `AbccoTeam3`
- Employees: Username is email prefix, Password is `<email_prefix><MMDDYYYY>` (DOB format)

#### `time_entries`

Stores daily time records for employees.

**Key Fields:**

- `time_entry_id` (INTEGER, Primary Key, Autoincrement)
- `employee_id` (TEXT, Foreign Key)
- `entry_date` (TEXT) - Date of work
- `hours_worked` (REAL) - Regular hours
- `overtime_hours` (REAL) - Overtime hours (>8 hrs/day or Saturday work)
- `pto_hours` (REAL) - PTO hours used
- `is_locked` (INTEGER) - Whether entry is locked after payroll calculation

**Business Rules:**

- Regular hours: Up to 8 hours/day
- Overtime: >8 hours/day or any Saturday hours (1.5x pay)
- PTO: Available for salaried and hourly employees

#### `pto_balances`

Tracks paid time off balances.

**Key Fields:**

- `pto_balance_id` (INTEGER, Primary Key, Autoincrement)
- `employee_id` (TEXT, Foreign Key, Unique)
- `total_accrued` (REAL) - Total PTO earned
- `total_used` (REAL) - Total PTO used
- `balance` (REAL) - Available PTO hours

**Constraints:**

- Balance cannot be negative
- Maximum balance: 80 hours

#### `payroll_periods`

Defines payroll calculation periods.

**Fields:**

- `payroll_period_id` (INTEGER, Primary Key, Autoincrement)
- `start_date` (TEXT) - Period start date
- `end_date` (TEXT) - Period end date
- `is_locked` (INTEGER) - Whether period is finalized

#### `payroll_details`

Stores calculated payroll for each employee and period.

**Key Fields:**

- `payroll_detail_id` (INTEGER, Primary Key, Autoincrement)
- `payroll_period_id` (INTEGER, Foreign Key)
- `employee_id` (TEXT, Foreign Key)
- `gross_pay` (REAL) - Total earnings before deductions
- `medical_deduction` (REAL)
- `dependent_stipend` (REAL)
- `state_tax` (REAL) - IN 3.15%
- `federal_tax_employee` (REAL) - 7.65%
- `federal_tax_employer` (REAL) - 7.65%
- `social_security_employee` (REAL) - 6.2%
- `social_security_employer` (REAL) - 6.2%
- `medicare_employee` (REAL) - 1.45%
- `medicare_employer` (REAL) - 1.45%
- `net_pay` (REAL) - Take-home pay

### Views

#### `vw_employee_full`

Comprehensive employee information view joining employees, departments, job titles, compensation, and PTO balances.

#### `vw_weekly_time_summary`

Weekly summary of time entries showing regular hours, overtime, and PTO.

### Indexes

Performance indexes are created on:

- Foreign key columns (for join performance)
- Email addresses (for lookups)
- Employee status (for filtering active/terminated)
- Time entry dates (for date range queries)

### Triggers

Automatic triggers maintain data integrity:

- Update employee last modified timestamps
- Update PTO balance when time entries change
- Validate compensation data consistency
- Enforce age requirements

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Standard library only (no external dependencies required)

### Initial Database Setup

Run the automated setup script to create the database with sample data:

```bash
# With UV
uv run setup_database.py

# Or with standard Python
python setup_database.py
```

This script will:

1. Create the SQLite database (`payroll.db`)
2. Execute the schema creation (`database/schema.sql`)
3. Load sample employee data from `database/sample_data.json`
4. Create user accounts for admin and all active employees
5. Initialize PTO balances

**Sample Data Includes:**

- 8 departments
- 12 job titles
- 12 employees (10 active, 2 terminated)
- Compensation records for all employees
- User accounts with default credentials

### Manual Setup (Alternative)

If you prefer to set up components individually:

```bash
# 1. Create database and schema
sqlite3 payroll.db < database/schema.sql

# 2. Load sample data
python database/load_test_data.py

# 3. Create user accounts
python database/auth.py
```

### Testing the Database

Verify the database setup with the test script:

```bash
# With UV
uv run database/test_database.py

# Or with standard Python
python database/test_database.py
```

This validates:

- Database file exists
- All required tables created
- Sample data loaded correctly
- User accounts created
- Authentication works

## Authentication System

### Password Generation

**Admin Account:**

- Username: `HR0001`
- Password: `AbccoTeam3`
- Type: Admin

**Employee Accounts:**

- Username: Email prefix (e.g., `roy.mustang` from `roy.mustang@abccompany.com`)
- Password: `<email_prefix><MMDDYYYY>` (e.g., `roy.mustang11062005`)
- Type: Employee

**Example:**

```sh
Email: roy.mustang@abccompany.com
DOB: 2005-11-06
Username: roy.mustang
Password: roy.mustang11062005
```

### Password Hashing

Current implementation (Week 4):

- SHA256 hashing for password storage
- No plaintext passwords in database

Future enhancement (Week 5+):

- Upgrade to bcrypt for enhanced security
- Add password salting

## Database Management

### Direct Database Access

You can inspect the database directly using SQLite:

```bash
sqlite3 payroll.db
```

Useful SQLite commands:

```sql
.tables                    -- List all tables
.schema employees          -- Show table structure
.mode column              -- Format output
.headers on               -- Show column headers

-- Query examples
SELECT * FROM employees WHERE status='Active';
SELECT * FROM vw_employee_full;
```

### Backup and Recovery

**Backup:**

```bash
# Copy database file
cp payroll.db payroll_backup_$(date +%Y%m%d).db

# Or use SQLite backup
sqlite3 payroll.db ".backup payroll_backup.db"
```

**Recovery:**

```bash
cp payroll_backup.db payroll.db
```

### Resetting the Database

To start fresh:

```bash
# Delete existing database
rm payroll.db

# Re-run setup
python setup_database.py
```

Or answer "yes" when setup script detects existing database.

## Sample Data

The system includes 12 test employees:

**Active Employees (10):**

- E001: Roy Mustang (IT, Salary)
- E002: Riza Hawkeye (IT, Hourly)
- E004: Edward Elric (Engineering, Salary)
- E005: Alphonse Elric (Engineering, Hourly)
- E006: Winry Rockbell (Operations, Salary)
- E007: Maes Hughes (HR, Salary)
- E008: Alex Armstrong (Operations, Hourly)
- E009: Olivier Armstrong (Executive, Salary)
- E010: Scar Johnson (Finance, Salary)
- E012: Ling Yao (Sales, Hourly)

**Terminated Employees (2):**

- E003: Salim Bradley (IT, Hourly)
- E011: Greed Smith (Marketing, Salary)

## Tax and Deduction Calculations

### Tax Rates

- **State Tax (Indiana):** 3.15% of gross pay
- **Federal Tax Employee:** 7.65% of gross pay
- **Federal Tax Employer:** 7.65% of gross pay
- **Social Security Employee:** 6.2% of gross pay
- **Social Security Employer:** 6.2% of gross pay
- **Medicare Employee:** 1.45% of gross pay
- **Medicare Employer:** 1.45% of gross pay

### Deduction Order

1. Medical deduction (pre-tax)
2. Dependent stipend (added, pre-tax)
3. Calculate taxes on adjusted gross
4. Calculate net pay

### Overtime Rules

- **Daily overtime:** Hours >8 in a day = 1.5x pay
- **Weekend overtime:** All Saturday hours = 1.5x pay
- **Salaried employees:** Automatically paid 8 hours Monday-Friday, can only enter PTO

## File Locations

```
SDEV268PayrollApplication/
├── database/
│   ├── schema.sql              # Database schema definition
│   ├── sample_data.json        # Test employee data
│   ├── load_test_data.py       # Data loading script
│   ├── auth.py                 # Authentication utilities
│   └── test_database.py        # Database validation script
├── setup_database.py           # One-command setup script
├── payroll.db                  # SQLite database (generated)
└── docs/
    └── database-setup.md       # This file
```

## Troubleshooting

### Database File Not Found

```bash
# Ensure you're in the project root directory
cd SDEV268PayrollApplication
python setup_database.py
```

### Permission Errors

Ensure you have write permissions in the project directory.

### Corrupted Database

Delete `payroll.db` and re-run `setup_database.py`.

### Import Errors

Ensure you're using Python 3.10+ and running scripts from the project root directory.

## Future Enhancements

- [ ] Upgrade to bcrypt password hashing
- [ ] Add database migration system
- [ ] Implement automatic backup system
- [ ] Add database connection pooling
- [ ] Create admin interface for database maintenance
- [ ] Add data export functionality (CSV, Excel)
- [ ] Implement audit logging for data changes

## Support

For questions or issues:

1. Check this documentation
2. Run the test script: `python database/test_database.py`
3. Review project README.md
4. Contact team members via GitHub issues
