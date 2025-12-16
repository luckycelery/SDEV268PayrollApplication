# ABC Payroll Python Project

A comprehensive payroll management system for ABC Company, built with Python and SQLite.

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Flask 3.1.2+ (installed via uv or pip)

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd SDEV268PayrollApplication
```

2. **Install dependencies**

Using UV (recommended):

```bash
uv sync
```

Or using pip:

```bash
pip install -r requirements.txt
```

### Database Setup

Set up the complete database with sample data in one command:

```bash
uv run python src/utils/setup_database.py
```

This creates the database, schema, sample employees, and user accounts automatically.

**Default Login Credentials:**

- Admin: `HR0001` / `AbccoTeam3`
- Employees: `<email>` / `<email_prefix><MMDDYYYY>`
  - Example (Salary): `roy.mustang@abccompany.com` / `roy.mustang11062005`
  - Example (Hourly): `juni.ito@abccompany.com` / `junji.ito02041994`

### Running the Application

Start the Flask web server:

```bash
python -m flask run
```

Or:

```bash
uv run python app.py
```

The application will be available at: <http://127.0.0.1:5000>

## Features

### Web-Based Interface

- **Modern Flask web application** with responsive HTML/CSS interface
- **Role-based access control** (Admin vs. Employee)
- **Session-based authentication** with secure password hashing

### Admin Functionality

- **Employee Management**: Add, edit, delete, and search employees
- **Payroll Management**: Calculate and process payroll for pay periods
- **Compensation Management**: Set and update salary/hourly rates and benefits
- **Time Entry Approval**: Review and adjust employee time entries
- **Reporting**: Generate payroll reports for HR sign-off

### Employee Functionality

- **Time Entry**: Submit daily hours worked and PTO requests
- **Paycheck Viewing**: View calculated paychecks with detailed breakdowns
- **PTO Balance**: Track available paid time off

### Automated Calculations

- **Gross Pay**: Regular hours + overtime (1.5x) + Saturday premium (1.5x)
- **Deductions**: Medical insurance, federal/state taxes, Social Security, Medicare
- **Dependent Stipend**: $45 per dependent per pay period
- **Tax Calculations**: Indiana state (3.15%), Federal (7.65%), SS (6.2%), Medicare (1.45%)

### Testing the Database

Verify everything is set up correctly:

```bash
uv run python database/test_database.py
```

For detailed database documentation, see [docs/database-setup.md](docs/database-setup.md).

## Project Structure

```sh
SDEV268PayrollApplication/
├── README.md                      # Project overview, setup instructions
├── pyproject.toml                 # Project configuration (UV/Ruff)
├── requirements.txt               # Pip dependencies (for non-UV users)
├── .gitignore                     # Ignore patterns
├── app.py                         # Flask application entry point
│
├── src/                           # Python source code
│   ├── __init__.py                # Flask application factory
│   ├── routes/                    # Flask route blueprints
│   │   ├── auth.py                # Login/logout routes
│   │   ├── admin.py               # Admin functionality routes
│   │   ├── employee.py            # Employee self-service routes
│   │   └── payroll.py             # Payroll management routes
│   ├── templates/                 # Jinja2 HTML templates
│   │   ├── base.html              # Base template with nav
│   │   ├── login.html             # Login page
│   │   ├── admin/                 # Admin templates
│   │   ├── employee/              # Employee templates
│   │   └── payroll/               # Payroll templates
│   ├── static/                    # Static assets (CSS, JS, images)
│   │   ├── css/                   # Stylesheets
│   │   ├── js/                    # JavaScript files
│   │   └── images/                # Images and logos
│   ├── models/                    # Data models (Employee, Payroll, etc.)
│   ├── controllers/               # Business logic and validation
│   └── utils/                     # Helper functions and constants
│       ├── constants.py           # Path configuration and constants
│       ├── setup_database.py      # Database initialization script
│       ├── load_time_entries.py   # Time entry data loader
│       └── calculate_payroll.py   # Payroll calculation utility
│
├── database/                      # Database files and utilities
│   ├── schema.sql                 # Database schema definition
│   ├── sample_data.json           # Test employee data
│   ├── load_data.py               # Data loading script
│   ├── auth.py                    # Authentication utilities
│   └── test_database.py           # Database validation tests
│
├── payroll.db                     # SQLite database (generated)
│
├── docs/                          # Documentation
│   ├── database-setup.md          # Database setup and reference
│   ├── project-plan.md            # Development plan
│   ├── uml-diagrams/              # UML diagrams for actors and classes
│   ├── user-guide.md              # User documentation
│   ├── security.md                # Security protocols
│   └── weekly-tasks.md            # 8-week development breakdown
│
├── testing/                       # Testing logs and screenshots
│   ├── initial-testing-log.md     # Pre-testing checklist
│   ├── final-testing-log.md       # Completed test results
│   ├── screenshots/               # Error messages, test results
│   └── test-cases.xlsx            # Test matrix
│
├── data/                          # Demo data for testing
│   └── sample_data.json           # 12 fictional employees
│
└── submission/                    # Final deliverables
    ├── payroll-report.pdf         # HR sign-off report
    └── payroll-output.txt         # Payroll output file
```

## Development Setup

This project supports both **UV** (fast, modern) and **pip** (traditional) workflows.

### Development Workflow

**Install dependencies:**

```bash
uv sync                                      # Using UV (recommended)
# or
pip install -r requirements.txt              # Using pip
```

**Database setup:**

```bash
uv run python src/utils/setup_database.py    # Initialize database
uv run python src/utils/load_time_entries.py # Load sample time entries
```

**Run the application:**

```bash
uv run flask run                             # Start Flask dev server
# or
uv run python app.py                         # Alternative entry point
```

**Code quality:**

```bash
ruff format .                                # Format code
ruff check --fix .                           # Fix linting issues
```

**Testing:**

```bash
pytest                                       # Run unit tests
uv run python database/test_database.py      # Database validation
```

For detailed setup instructions, see [docs/development-setup.md](docs/development-setup.md).

## Database Overview

The system uses SQLite with the following core tables:

- **employees** - Personal info, job title, pay type, status
- **departments** - Organizational departments
- **job_titles** - Job position definitions
- **compensation** - Salary/hourly rates, benefits
- **users** - Login credentials and roles (admin, employee)
- **time_entries** - Daily hours, PTO, overtime tracking
- **pto_balances** - Paid time off balances
- **payroll_periods** - Pay period definitions
- **payroll_details** - Calculated salary, deductions, taxes, net pay

**Sample Data:** 12 employees (10 active, 2 terminated) across 8 departments with 12 job titles.

For complete database documentation, see [docs/database-setup.md](docs/database-setup.md).

