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
  - Example: `roy.mustang@abccompany.com` / `roy.mustang11062005`

### Running the Application

Start the Flask web server:

```bash
uv run flask run
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

{MISC INFO ABOUT PROJECT AND REQUIREMENTS}

- will use sql lite
- HR001 admin cred with secure pw

- need to dev UML diagrams
- sketch designs finalize and input into user doc
- need to create template for project plan combined (include types of algorithms used) - with user doc (use past one for reference)
                *Develop a detailed plan outlining the steps you will use to create your
                  program. This should include the number of menus, and screens required,
                  database creation and the type of database you use in your project and what
                  algorithms will be employed in the development project, providing a rationale
                  for their selection.
                o You will need to identify the types of actors that will use your application and
                  produce UML diagrams for all actors involved in the application to clearly
                  define their roles and responsibilities.
                o Include a breakdown of tasks to be completed over the next eight weeks as
                  part of the project plan.
                o Prepare user-friendly documentation for the application to facilitate user
                  understanding of its features and functionalities.
                o Follow good program standards by storing and defining your variables
                  establishing security and how you will be protecting the sensitive data entered
                  in the payroll system
                * proof of security measures included in this too - probalby will be a screenshot
                * Your plan should carefully detail the structure and organization of the
                database to guarantee optimal functionality.

- develop testing log based on UML diagrams to test different scenarious methodically
              * Establish a structured testing log to methodically test the application's various
                  scenarios. Your testing log should be thoroughly checked to make sure there
                  is validation in place to protect the user from making errors.
              o Use the testing log to verify the accuracy of all calculations in the application,
                  particularly in relation to employee payments and taxes. You should provide
                  screenshots where you can show that your testing scenarios passed. For
                  example, your screenshot should display error messages, etc.
              o Create a minimum of 12 fabricated employee profiles within the application for
                  testing and demonstration purposes.
              o Your documentation posted in GitHub should contain your initial testing log
                  and then a completed log to show your log was available before the testing
                  began.

The main screen should feature the following options:

1. Login
2. User ID and Password Entry
3. User Type Selection (Admin or Employee)
4. Exit Program
Once a user has successfully logged in:

- For Admin users:
- Employee demographics access
- Payroll information access / Calculate payroll
- Adding, editing, and deleting options available
- Employee search function
- Reporting
- Application information (version number)
- For Employee users:
- Hours worked entry functionality
- PTO (personal time off) option
- Paycheck calculation feature
As the project progresses, new steps and updates will be integrated into each module,
enhancing, and refining the plan based on knowledge gained from previous and current
courses.
Employee Screen
• Only accessible by the admin login.
• Adding, editing, or deleting an employee record
• Fields that are required and should apply appropriate validation.
o Employee ID
o Department, Job Title
o First Name, Last Name, Sur Name
o Status (active or terminated)
o Date of Birth (must be at least 18 years of age)
o Gender (Male or Female)
o Pay type (Salary or Hourly)
o Company email
o Address Line 1, Address Line 2
o City, State, or Zip
o Employee picture when available
Salary Screen
• Only accessible by the admin login.
• Current information should be displayed on the screen to support any salary.
o Department
o Job Type Title
o First Name and Last Name
o Status
o Date Hire
o Salary Type
o Base Salary
o Medical (Single or Family Coverage)
o # of Dependents
Make sure you include the appropriate validations and checks. Items listed are the
minimum validations.
Employee Time Entry Screen
• Add by the employee.
• Edit until the payroll has been submitted.
• Admin - can adjust based on issues with previous payrolls.
• If the employee's pay is salary,
o The only entry will be to add PTO. Otherwise, they should
automatically be paid 8 hours on Monday or Friday.
• If the employee's pay is hourly,
o The employee should be able to enter the total number for the day.
o the system should calculate overtime based on an 8-hour-a-day
(anything over 8 hours should pay time and a half.
o The system should be able to collect hours worked for 7 days
(anytime on Saturday should pay time and a half.
• Medical is calculated at $50 for single coverage and $100 for family
coverage.
• The employee is given a $45 stipend for each dependent.
• The screen should show the employee's medical, dependent stipend, taxes
for state, federal, Medicare, and social security deduction amounts for both
the employee and the employer.
• State tax, IN 3.15%
• Federal tax Employee 7.65%, Employer 7.65%
• Social Security tax Employee 6.2%, Employer 6.2%
• Medicare Employee 1.45%, Employer 1.45%
Admin Options and Calculating Payroll
• Only accessible by the admin login
• Calculate the payroll.
o Lock the work entry so there are no updates after the calculated payroll
has been selected.
o Calculate the gross payroll.
o Calculate the net payroll.
o Create a report for HR to sign off.
o Create a file for the payroll department to see to the printer after sign-off.
Hint: all deductions should be on a pretax basis, i.e., the medical should be deducted
before calculating state, federal, or other taxes.

**The program should include arrays or lists for managing data entry, insertion, and deletion, demonstrating your proficiency in the techniques covered in the course. Showcase your dedication and skills as you develop
this application.**

A comprehensive plan must be established to begin the payroll program's development
process. This plan should include tasks such as collecting hours worked, calculating
taxes, designing the screens, determining the information to be captured, designing the
database, and other relevant activities. It is crucial to review all input data and identify
any inconsistencies carefully. For instance, if the standard work hours are 40 hours per
week, submitting 80 hours would be considered unusual and should be addressed
promptly.
A minimum of twelve employees should be designated for use in test cases. Your
responsibilities will involve creating documentation to support the development plan and
providing guidance to users after the application is completed. Additionally, you will be
responsible for designing and developing the Java-based application.
All program files and documentation should be organized within GitHub. Your final
submission will be a link to your GitHub repository, where the instructor will grade your
project. Make sure you give your instructor access to your GitHub so there will not be an
access issue when they go to grade the final submissions.
