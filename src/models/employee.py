"""
Employee Model - Represents employee business object and database operations
Matches the actual database schema in database/schema.sql
"""

import sqlite3
from datetime import date, datetime
from typing import Optional

from src.utils.constants import (
    EMPLOYEE_STATUS_ACTIVE,
    EMPLOYEE_STATUS_TERMINATED,
    GENDER_FEMALE,
    GENDER_MALE,
    MEDICAL_TYPE_SINGLE,
    MIN_EMPLOYEE_AGE,
    SALARY_TYPE_HOURLY,
    SALARY_TYPE_SALARY,
    VALID_GENDERS,
    VALID_MEDICAL_TYPES,
    VALID_SALARY_TYPES,
)

from .base_model import BaseModel


class Employee(BaseModel):
    """
    Employee model - handles employee data and database operations

    Matches the database schema:
    - employees table: Core employee data including address
    - compensation table: Salary/hourly rate, medical, dependents
    - Uses vw_employee_full view for complete data retrieval
    """

    # Database view for all employee read operations
    _EMPLOYEE_VIEW = "vw_employee_full"

    def __init__(
        self,
        employee_id: str,
        first_name: str,
        last_name: str,
        date_of_birth: str,
        gender: str,
        email: str,
        address_line1: str,
        city: str,
        state: str,
        zip_code: str,
        date_hired: str,
        department_name: str,
        job_title_name: str,
        # Optional fields
        surname: str | None = None,
        phone_num: str | None = None,
        address_line2: str | None = None,
        has_picture: int = 0,
        picture_filename: str | None = None,
        status: str = EMPLOYEE_STATUS_ACTIVE,
        # Compensation fields (from compensation table)
        salary_type: str | None = None,
        base_salary: float | None = None,
        hourly_rate: float | None = None,
        medical_type: str | None = None,
        num_dependents: int = 0,
        # PTO fields (from pto_balances table)
        pto_accrued: float = 0.0,
        pto_used: float = 0.0,
        pto_balance: float = 0.0,
    ):
        """
        Initialize Employee object matching database schema.

        Args:
            employee_id: Unique employee identifier (e.g., 'E001')
            first_name: Employee's first name
            last_name: Employee's last name
            date_of_birth: Date of birth (YYYY-MM-DD)
            gender: 'Male' or 'Female'
            email: Company email address (unique)
            address_line1: Street address
            city: City name
            state: State abbreviation
            zip_code: ZIP code
            date_hired: Hire date (YYYY-MM-DD)
            department_name: Department name (FK to departments)
            job_title_name: Job title (FK to job_titles)
            surname: Employee's surname/suffix (Jr., Sr., etc.)
            address_line2: Apt/Suite number (optional)
            has_picture: 1 or 0 indicating if photo available
            picture_filename: Filename of employee picture
            status: 'Active' or 'Terminated'
            salary_type: 'Salary' or 'Hourly'
            base_salary: Annual salary (for salaried employees)
            hourly_rate: Hourly rate (for hourly employees)
            medical_type: 'Single' or 'Family'
            num_dependents: Number of dependents
            pto_accrued: Total PTO hours accrued/granted
            pto_used: Total PTO hours used
            pto_balance: Current PTO balance in hours (accrued - used)
        """
        # Core employee fields
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.email = email
        self.phone_num = phone_num

        # Address fields (inline in employees table)
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.city = city
        self.state = state
        self.zip_code = zip_code

        # Employment info
        self.has_picture = has_picture
        self.picture_filename = picture_filename
        self.status = status
        self.date_hired = date_hired
        self.department_name = department_name
        self.job_title_name = job_title_name

        # Compensation fields (from compensation table)
        self.salary_type = salary_type
        self.base_salary = base_salary
        self.hourly_rate = hourly_rate
        self.medical_type = medical_type
        self.num_dependents = num_dependents

        # PTO fields (from pto_balances table)
        self.pto_accrued = pto_accrued
        self.pto_used = pto_used
        self.pto_balance = pto_balance

    # ==================== BUSINESS LOGIC ====================

    def calculate_age(self, as_of_date: date | None = None) -> int:
        """
        Calculate employee age from date of birth.

        Args:
            as_of_date: Date to calculate age as of (default: today)

        Returns:
            Age in years
        """
        if as_of_date is None:
            as_of_date = date.today()

        birth_date = datetime.strptime(self.date_of_birth, "%Y-%m-%d").date()
        age = as_of_date.year - birth_date.year

        # Adjust if birthday hasn't occurred yet this year
        if as_of_date.month < birth_date.month or (
            as_of_date.month == birth_date.month and as_of_date.day < birth_date.day
        ):
            age -= 1

        return age

    def get_full_name(self) -> str:
        """
        Get employee's full name with surname if present.

        Returns:
            Full name string
        """
        if self.surname:
            return f"{self.first_name} {self.last_name} {self.surname}"
        return f"{self.first_name} {self.last_name}"

    def is_active(self) -> bool:
        """Check if employee status is active."""
        return self.status == EMPLOYEE_STATUS_ACTIVE

    def is_salaried(self) -> bool:
        """Check if employee is salaried (vs hourly)."""
        return self.salary_type == SALARY_TYPE_SALARY

    def get_pay_rate(self) -> float:
        """
        Get the employee's pay rate.

        Returns:
            base_salary for salaried, hourly_rate for hourly employees
        """
        if self.is_salaried():
            return self.base_salary or 0.0
        return self.hourly_rate or 0.0

    # ==================== VALIDATION ====================

    def validate(self) -> tuple[bool, list[str]]:
        """
        Validate employee data against business rules.

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Required field validation
        if not self.employee_id or not self.employee_id.strip():
            errors.append("Employee ID is required")

        if not self.first_name or not self.first_name.strip():
            errors.append("First name is required")

        if not self.last_name or not self.last_name.strip():
            errors.append("Last name is required")

        if not self.date_of_birth:
            errors.append("Date of birth is required")

        if not self.gender or self.gender not in VALID_GENDERS:
            errors.append(f"Gender must be '{GENDER_MALE}' or '{GENDER_FEMALE}'")

        if not self.email or not self.email.strip():
            errors.append("Email is required")
        elif "@" not in self.email:
            errors.append("Invalid email format")

        valid_statuses = (EMPLOYEE_STATUS_ACTIVE, EMPLOYEE_STATUS_TERMINATED)
        if not self.status or self.status not in valid_statuses:
            errors.append(f"Status must be '{EMPLOYEE_STATUS_ACTIVE}' or '{EMPLOYEE_STATUS_TERMINATED}'")

        # Address validation
        if not self.address_line1 or not self.address_line1.strip():
            errors.append("Address line 1 is required")

        if not self.city or not self.city.strip():
            errors.append("City is required")

        if not self.state or not self.state.strip():
            errors.append("State is required")

        if not self.zip_code or not self.zip_code.strip():
            errors.append("ZIP code is required")

        # Age validation (must be MIN_EMPLOYEE_AGE+)
        try:
            age = self.calculate_age()
            if age < MIN_EMPLOYEE_AGE:
                errors.append(f"Employee must be at least {MIN_EMPLOYEE_AGE} years old (current age: {age})")
        except (ValueError, TypeError):
            errors.append("Invalid date of birth format (use YYYY-MM-DD)")

        # Date hired validation (cannot be future date)
        if self.date_hired:
            try:
                hire_date = datetime.strptime(self.date_hired, "%Y-%m-%d").date()
                if hire_date > date.today():
                    errors.append("Hire date cannot be in the future")
            except (ValueError, TypeError):
                errors.append("Invalid hire date format (use YYYY-MM-DD)")

        # Compensation validation
        if self.salary_type and self.salary_type not in VALID_SALARY_TYPES:
            errors.append(f"Salary type must be '{SALARY_TYPE_SALARY}' or '{SALARY_TYPE_HOURLY}'")

        if self.salary_type == SALARY_TYPE_SALARY:
            if self.base_salary is None or self.base_salary <= 0:
                errors.append("Base salary must be greater than 0 for salaried employees")
        elif self.salary_type == SALARY_TYPE_HOURLY:
            if self.hourly_rate is None or self.hourly_rate <= 0:
                errors.append("Hourly rate must be greater than 0 for hourly employees")

        if self.medical_type and self.medical_type not in VALID_MEDICAL_TYPES:
            errors.append(f"Medical type must be '{MEDICAL_TYPE_SINGLE}' or 'Family'")

        if self.num_dependents < 0:
            errors.append("Number of dependents cannot be negative")

        return (len(errors) == 0, errors)

    # ==================== DATABASE OPERATIONS ====================

    @classmethod
    def get_by_id(cls, employee_id: str) -> Optional["Employee"]:
        """
        Retrieve employee by ID using the vw_employee_full view.

        Args:
            employee_id: Employee ID to retrieve

        Returns:
            Employee object or None if not found
        """
        query = f"SELECT * FROM {cls._EMPLOYEE_VIEW} WHERE employee_id = ?"
        row = cls.execute_single(query, (employee_id,))

        if row:
            return cls._from_row(row)
        return None

    @classmethod
    def get_all(cls, include_terminated: bool = False) -> list["Employee"]:
        """
        Retrieve all employees.

        Args:
            include_terminated: Include terminated employees (default: False)

        Returns:
            List of Employee objects
        """
        query = f"SELECT * FROM {cls._EMPLOYEE_VIEW}"

        if not include_terminated:
            query += " WHERE status = 'Active'"

        query += " ORDER BY last_name, first_name"

        rows = cls.execute_query(query)
        return [cls._from_row(row) for row in rows]

    @classmethod
    def search(cls, search_term: str) -> list["Employee"]:
        """
        Search employees by name, email, or ID.

        Args:
            search_term: Text to search for

        Returns:
            List of matching Employee objects
        """
        query = f"""
            SELECT * FROM {cls._EMPLOYEE_VIEW}
            WHERE employee_id LIKE ?
               OR first_name LIKE ?
               OR last_name LIKE ?
               OR email LIKE ?
            ORDER BY last_name, first_name
        """
        search_pattern = f"%{search_term}%"
        rows = cls.execute_query(
            query, (search_pattern, search_pattern, search_pattern, search_pattern)
        )
        return [cls._from_row(row) for row in rows]

    @classmethod
    def get_by_department(cls, department: str) -> list["Employee"]:
        """
        Get all active employees in a department.

        Args:
            department: Department name

        Returns:
            List of Employee objects
        """
        query = f"""
            SELECT * FROM {cls._EMPLOYEE_VIEW}
            WHERE department_name = ? AND status = 'Active'
            ORDER BY last_name, first_name
        """
        rows = cls.execute_query(query, (department,))
        return [cls._from_row(row) for row in rows]

    def save(self) -> bool:
        """
        Save employee to database (insert or update).
        Saves to employees and compensation tables.

        Returns:
            True if successful

        Raises:
            ValueError: If validation fails
        """
        # First validate
        is_valid, errors = self.validate()
        if not is_valid:
            raise ValueError(f"Validation failed: {', '.join(errors)}")

        # Check if employee exists
        existing = self.get_by_id(self.employee_id)

        if existing:
            return self._update()
        else:
            return self._insert()

    def _insert(self) -> bool:
        """Insert new employee into database."""
        # Insert into employees table
        employee_query = """
            INSERT INTO employees (
                employee_id, first_name, last_name, surname, date_of_birth, gender,
                email, phone_num, address_line1, address_line2, city, state, zip_code,
                has_picture, picture_filename, status, date_hired,
                department_name, job_title_name
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute_write(
            employee_query,
            (
                self.employee_id,
                self.first_name,
                self.last_name,
                self.surname,
                self.date_of_birth,
                self.gender,
                self.email,
                self.phone_num,
                self.address_line1,
                self.address_line2,
                self.city,
                self.state,
                self.zip_code,
                self.has_picture,
                self.picture_filename,
                self.status,
                self.date_hired,
                self.department_name,
                self.job_title_name,
            ),
        )

        # Insert into compensation table if compensation data provided
        if self.salary_type:
            comp_query = """
                INSERT INTO compensation (
                    employee_id, salary_type, base_salary, hourly_rate,
                    medical_type, num_dependents, effective_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            self.execute_write(
                comp_query,
                (
                    self.employee_id,
                    self.salary_type,
                    self.base_salary,
                    self.hourly_rate,
                    self.medical_type or MEDICAL_TYPE_SINGLE,
                    self.num_dependents,
                    self.date_hired,
                ),
            )

        return True

    def _update(self) -> bool:
        """Update existing employee in database."""
        # Update employees table
        employee_query = """
            UPDATE employees SET
                first_name = ?, last_name = ?, surname = ?, date_of_birth = ?,
                gender = ?, email = ?, phone_num = ?, address_line1 = ?, address_line2 = ?,
                city = ?, state = ?, zip_code = ?, has_picture = ?,
                picture_filename = ?, status = ?, date_hired = ?,
                department_name = ?, job_title_name = ?
            WHERE employee_id = ?
        """
        self.execute_write(
            employee_query,
            (
                self.first_name,
                self.last_name,
                self.surname,
                self.date_of_birth,
                self.gender,
                self.email,
                self.phone_num,
                self.address_line1,
                self.address_line2,
                self.city,
                self.state,
                self.zip_code,
                self.has_picture,
                self.picture_filename,
                self.status,
                self.date_hired,
                self.department_name,
                self.job_title_name,
                self.employee_id,
            ),
        )

        # Update or insert compensation
        if self.salary_type:
            comp_check = "SELECT employee_id FROM compensation WHERE employee_id = ?"
            existing_comp = self.execute_single(comp_check, (self.employee_id,))

            if existing_comp:
                comp_query = """
                    UPDATE compensation SET
                        salary_type = ?, base_salary = ?, hourly_rate = ?,
                        medical_type = ?, num_dependents = ?
                    WHERE employee_id = ?
                """
                self.execute_write(
                    comp_query,
                    (
                        self.salary_type,
                        self.base_salary,
                        self.hourly_rate,
                        self.medical_type,
                        self.num_dependents,
                        self.employee_id,
                    ),
                )
            else:
                comp_query = """
                    INSERT INTO compensation (
                        employee_id, salary_type, base_salary, hourly_rate,
                        medical_type, num_dependents, effective_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                self.execute_write(
                    comp_query,
                    (
                        self.employee_id,
                        self.salary_type,
                        self.base_salary,
                        self.hourly_rate,
                        self.medical_type or MEDICAL_TYPE_SINGLE,
                        self.num_dependents,
                        self.date_hired,
                    ),
                )

        return True

    def delete(self) -> bool:
        """
        Soft delete employee (set status to Terminated).

        Returns:
            True if successful
        """
        query = f"UPDATE employees SET status = '{EMPLOYEE_STATUS_TERMINATED}' WHERE employee_id = ?"
        self.execute_write(query, (self.employee_id,))
        self.status = EMPLOYEE_STATUS_TERMINATED
        return True

    @classmethod
    def hard_delete(cls, employee_id: str) -> bool:
        """
        Permanently delete employee from database.
        WARNING: This cascades to compensation, time_entries, and payroll!

        Args:
            employee_id: Employee ID to delete

        Returns:
            True if successful
        """
        # Delete compensation first (no cascade in schema)
        cls.execute_write("DELETE FROM compensation WHERE employee_id = ?", (employee_id,))
        cls.execute_write("DELETE FROM pto_balances WHERE employee_id = ?", (employee_id,))
        cls.execute_write("DELETE FROM employees WHERE employee_id = ?", (employee_id,))
        return True

    # ==================== HELPER METHODS ====================

    @classmethod
    def _from_row(cls, row: sqlite3.Row) -> "Employee":
        """
        Create Employee object from database row.

        Args:
            row: sqlite3.Row object

        Returns:
            Employee object
        """
        return cls(
            employee_id=row["employee_id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            surname=row["surname"],
            date_of_birth=row["date_of_birth"],
            gender=row["gender"],
            email=row["email"],
            address_line1=row["address_line1"],
            address_line2=row["address_line2"],
            city=row["city"],
            state=row["state"],
            zip_code=row["zip_code"],
            phone_num=row["phone_num"],
            has_picture=row["has_picture"],
            picture_filename=row["picture_filename"],
            status=row["status"],
            date_hired=row["date_hired"],
            department_name=row["department_name"],
            job_title_name=row["job_title_name"],
            salary_type=row["salary_type"],
            base_salary=row["base_salary"],
            hourly_rate=row["hourly_rate"],
            medical_type=row["medical_type"],
            num_dependents=row["num_dependents"] or 0,
            pto_accrued=row["pto_accrued"] or 0.0,
            pto_used=row["pto_used"] or 0.0,
            pto_balance=row["pto_balance"] or 0.0,
        )

    def to_dict(self) -> dict:
        """
        Convert employee to dictionary.

        Returns:
            Dictionary representation of employee
        """
        return {
            "employee_id": self.employee_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "surname": self.surname,
            "full_name": self.get_full_name(),
            "date_of_birth": self.date_of_birth,
            "age": self.calculate_age(),
            "gender": self.gender,
            "email": self.email,
            "address_line1": self.address_line1,
            "address_line2": self.address_line2,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "phone_num": self.phone_num,
            "has_picture": self.has_picture,
            "picture_filename": self.picture_filename,
            "status": self.status,
            "date_hired": self.date_hired,
            "department_name": self.department_name,
            "job_title_name": self.job_title_name,
            "salary_type": self.salary_type,
            "base_salary": self.base_salary,
            "hourly_rate": self.hourly_rate,
            "pay_rate": self.get_pay_rate(),
            "medical_type": self.medical_type,
            "num_dependents": self.num_dependents,
            "pto_accrued": self.pto_accrued,
            "pto_used": self.pto_used,
            "pto_balance": self.pto_balance,
            "is_active": self.is_active(),
            "is_salaried": self.is_salaried(),
        }

    def __repr__(self) -> str:
        """String representation of employee."""
        return f"Employee({self.employee_id}: {self.get_full_name()}, {self.job_title_name})"
