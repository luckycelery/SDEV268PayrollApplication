"""
Graceful data loader - loads valid records, reports invalid ones
Continues on errors instead of stopping the entire process
Uses only ASCII characters for terminal compatibility
"""
import json
import sqlite3
from datetime import datetime


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class DataLoadReport:
    """Track loading results for all data types"""
    def __init__(self):
        # Department tracking
        self.departments_loaded = 0
        self.departments_failed: list[tuple[str, str]] = []

        # Job title tracking
        self.job_titles_loaded = 0
        self.job_titles_failed: list[tuple[str, str]] = []

        # Employee tracking
        self.employees_loaded = 0
        self.employees_failed: list[tuple[str, str, str]] = []

        # Compensation tracking
        self.compensation_loaded = 0
        self.compensation_failed: list[tuple[str, str]] = []

    def print_summary(self):
        """Print comprehensive loading summary"""
        print("\n" + "=" * 70)
        print("DATABASE LOADING SUMMARY")
        print("=" * 70)

        # Departments
        print(f"\nDepartments: {self.departments_loaded} loaded")
        if self.departments_failed:
            print(f"  [FAILED] {len(self.departments_failed)} department(s):")
            for dept, error in self.departments_failed:
                print(f"    - {dept}: {error}")

        # Job Titles
        print(f"\nJob Titles: {self.job_titles_loaded} loaded")
        if self.job_titles_failed:
            print(f"  [FAILED] {len(self.job_titles_failed)} job title(s):")
            for title, error in self.job_titles_failed:
                print(f"    - {title}: {error}")

        # Employees (most important)
        print(f"\nEmployees: {self.employees_loaded} loaded")
        if self.employees_failed:
            print(f"  [FAILED] {len(self.employees_failed)} employee(s):")
            for emp_id, name, error in self.employees_failed:
                print(f"    - {emp_id} ({name}): {error}")

        # Compensation
        print(f"\nCompensation Records: {self.compensation_loaded} loaded")
        if self.compensation_failed:
            print(f"  [FAILED] {len(self.compensation_failed)} compensation record(s):")
            for emp_id, error in self.compensation_failed:
                print(f"    - {emp_id}: {error}")

        # Overall status
        print("\n" + "=" * 70)
        total_failed = (len(self.departments_failed) +
                       len(self.job_titles_failed) +
                       len(self.employees_failed) +
                       len(self.compensation_failed))

        if total_failed > 0:
            print(f"WARNING: {total_failed} total validation error(s) found!")
            print("These errors prove your validation logic is working correctly.")
        else:
            print("SUCCESS: All records loaded without errors!")
        print("=" * 70 + "\n")


def validate_employee_age(dob_str: str, employee_name: str) -> None:
    """
    Validate employee is at least 18 years old

    Args:
        dob_str: Date of birth in YYYY-MM-DD format
        employee_name: Name for error message

    Raises:
        ValidationError: If employee is under 18
    """
    dob = datetime.strptime(dob_str, '%Y-%m-%d')
    today = datetime.now()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    if age < 18:
        raise ValidationError(f"Employee must be at least 18 years old (currently {age})")


def validate_hire_date(hire_date_str: str) -> None:
    """
    Validate hire date is not in the future

    Args:
        hire_date_str: Hire date in YYYY-MM-DD format

    Raises:
        ValidationError: If hire date is in the future
    """
    hire_date = datetime.strptime(hire_date_str, '%Y-%m-%d')
    today = datetime.now()

    if hire_date > today:
        raise ValidationError(f"Hire date cannot be in the future ({hire_date_str})")


def load_departments(conn: sqlite3.Connection, data: dict, report: DataLoadReport) -> None:
    """Load departments with error handling"""
    cursor = conn.cursor()
    print("\nLoading departments...")

    for dept in data.get('departments', []):
        dept_name = dept.get('department_name', 'UNKNOWN')
        try:
            cursor.execute(
                "INSERT INTO departments (department_name) VALUES (?)",
                (dept_name,)
            )
            conn.commit()
            report.departments_loaded += 1
            print(f"  [OK] {dept_name}")
        except Exception as e:
            conn.rollback()
            error_msg = str(e)
            report.departments_failed.append((dept_name, error_msg))
            print(f"  [FAIL] {dept_name}: {error_msg}")


def load_job_titles(conn: sqlite3.Connection, data: dict, report: DataLoadReport) -> None:
    """Load job titles with error handling"""
    cursor = conn.cursor()
    print("\nLoading job titles...")

    for title in data.get('job_titles', []):
        title_name = title.get('title_name', 'UNKNOWN')
        try:
            cursor.execute(
                "INSERT INTO job_titles (title_name) VALUES (?)",
                (title_name,)
            )
            conn.commit()
            report.job_titles_loaded += 1
            print(f"  [OK] {title_name}")
        except Exception as e:
            conn.rollback()
            error_msg = str(e)
            report.job_titles_failed.append((title_name, error_msg))
            print(f"  [FAIL] {title_name}: {error_msg}")


def load_employees(conn: sqlite3.Connection, data: dict, report: DataLoadReport) -> None:
    """Load employees with comprehensive validation and error handling"""
    cursor = conn.cursor()
    print("\nLoading employees...")

    for emp in data.get('employees', []):
        emp_id = emp.get('employee_id', 'UNKNOWN')
        emp_name = f"{emp.get('first_name', '')} {emp.get('last_name', '')}".strip()

        try:
            # Validate required fields
            if not emp.get('gender'):
                raise ValidationError("Gender is required")

            # Validate age (must be 18+)
            validate_employee_age(emp['date_of_birth'], emp_name)

            # Validate hire date (cannot be in future)
            validate_hire_date(emp['date_hired'])

            # Insert employee record
            cursor.execute("""
                INSERT INTO employees (
                    employee_id, first_name, last_name, surname,
                    date_of_birth, gender, email,
                    address_line1, address_line2, city, state, zip_code,
                    has_picture, picture_filename, status, date_hired,
                    department_name, job_title_name
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                emp['employee_id'],
                emp['first_name'],
                emp['last_name'],
                emp.get('surname'),
                emp['date_of_birth'],
                emp['gender'],
                emp['email'],
                emp['address_line1'],
                emp.get('address_line2'),
                emp['city'],
                emp['state'],
                emp['zip_code'],
                emp['has_picture'],
                emp.get('picture_filename'),
                emp['status'],
                emp['date_hired'],
                emp['department_name'],
                emp['job_title_name']
            ))
            conn.commit()
            report.employees_loaded += 1
            print(f"  [OK] {emp_id}: {emp_name}")

        except ValidationError as ve:
            conn.rollback()
            error_msg = str(ve)
            report.employees_failed.append((emp_id, emp_name, error_msg))
            print(f"  [FAIL] {emp_id} ({emp_name}): {error_msg}")

        except Exception as e:
            conn.rollback()
            error_msg = str(e)
            report.employees_failed.append((emp_id, emp_name, error_msg))
            print(f"  [FAIL] {emp_id} ({emp_name}): {error_msg}")


def load_compensation(conn: sqlite3.Connection, data: dict, report: DataLoadReport) -> None:
    """Load compensation records with error handling"""
    cursor = conn.cursor()
    print("\nLoading compensation records...")

    for comp in data.get('compensation', []):
        emp_id = comp.get('employee_id', 'UNKNOWN')

        try:
            # Check if employee exists first
            cursor.execute(
                "SELECT employee_id FROM employees WHERE employee_id = ?",
                (emp_id,)
            )
            if not cursor.fetchone():
                raise ValidationError(f"Employee {emp_id} not found (may have failed validation)")

            cursor.execute("""
                INSERT INTO compensation (
                    employee_id, salary_type, base_salary, hourly_rate,
                    medical_type, num_dependents, effective_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                emp_id,
                comp['salary_type'],
                comp.get('base_salary'),
                comp.get('hourly_rate'),
                comp['medical_type'],
                comp['num_dependents'],
                comp['effective_date']
            ))
            conn.commit()
            report.compensation_loaded += 1
            print(f"  [OK] {emp_id}")

        except ValidationError as ve:
            conn.rollback()
            error_msg = str(ve)
            report.compensation_failed.append((emp_id, error_msg))
            print(f"  [FAIL] {emp_id}: {error_msg}")

        except Exception as e:
            conn.rollback()
            error_msg = str(e)
            report.compensation_failed.append((emp_id, error_msg))
            print(f"  [FAIL] {emp_id}: {error_msg}")


def load_test_data(db_path: str, json_path: str) -> DataLoadReport:
    """
    Load test data from JSON file with graceful error handling

    Args:
        db_path: Path to SQLite database
        json_path: Path to JSON data file

    Returns:
        DataLoadReport with loading statistics
    """
    # Load JSON data
    with open(json_path) as f:
        data = json.load(f)

    # Connect to database
    conn = sqlite3.connect(db_path)
    report = DataLoadReport()

    try:
        # Load data in dependency order
        load_departments(conn, data, report)
        load_job_titles(conn, data, report)
        load_employees(conn, data, report)
        load_compensation(conn, data, report)

    finally:
        conn.close()

    return report


if __name__ == "__main__":
    # Example usage
    db_path = "payroll.db"
    json_path = "database/sample_data.json"

    print("Starting graceful data load...")
    print("This will load valid records and report invalid ones.\n")

    report = load_test_data(db_path, json_path)
    report.print_summary()
