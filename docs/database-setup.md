# Database Setup

## Overview

The ABC Payroll System uses SQLite to store employee information, compensation, user accounts, time entries, and payroll records.

## What's in the Database

**Main Tables:**

- `employees` - Employee demographics and employment info
- `departments` and `job_titles` - Reference data
- `compensation` - Salary/hourly rates and benefits
- `users` - Login credentials
- `time_entries` - Daily work hours and PTO
- `pto_balances` - PTO tracking
- `payroll_periods` and `payroll_details` - Payroll calculations

**Business Rules:**


- Medical: $50 (Single) or $100 (Family) per pay period
- Dependent stipend: $45 per dependent
- Overtime: >8 hours/day or Saturday hours = 1.5x pay
- Tax rates: IN 3.15%, Federal 7.65%, Social Security 6.2%, Medicare 1.45%

## Quick Setup

**One command to set up everything:**

```bash
python setup_database.py

# Or with UV:
uv run setup_database.py
```

This creates `payroll.db` with:

- 8 departments, 12 job titles
- 12 sample employees (10 active, 2 terminated)
- All compensation and user accounts

**To verify setup:**

```bash
python database/test_database.py

# Or with UV:
uv run database/test_database.py
```

**To reset database:**

```bash
Remove-Item payroll.db
python setup_database.py
```

## Login Credentials

**Admin:**

- Username: `HR0001`
- Password: `AbccoTeam3`

**Employees:**

- Username: Email prefix (e.g., `roy.mustang`)
- Password: `<email_prefix><MMDDYYYY>` (e.g., `roy.mustang11062005`)

Passwords are hashed with SHA256 before storage.

## Sample Data

Includes 12 test employees like Roy Mustang (IT), Riza Hawkeye (IT), Edward Elric (Engineering), etc. Mix of salary/hourly, active/terminated employees across all departments.
