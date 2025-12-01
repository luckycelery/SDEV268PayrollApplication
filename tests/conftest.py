"""
Pytest configuration and shared fixtures for payroll system tests.
"""

import os
import shutil

import pytest

from src.models.base_model import BaseModel


@pytest.fixture(scope="session")
def test_db_path(tmp_path_factory):
    """
    Create a test database path.
    Uses the production database as a template for integration tests.
    """
    # For integration tests, use a copy of the real database
    original_db = "payroll.db"
    test_db = tmp_path_factory.mktemp("data") / "test_payroll.db"

    if os.path.exists(original_db):
        shutil.copy(original_db, test_db)
    else:
        # If no production DB exists, tests requiring DB will fail appropriately
        pass

    return str(test_db)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db(test_db_path):
    """
    Configure the application to use the test database.
    Scoped to session so it runs once for all tests.
    autouse=True means it runs automatically for all tests.
    """
    # Save original path
    original_path = BaseModel.DB_PATH

    # Set test database
    BaseModel.set_db_path(test_db_path)

    yield test_db_path

    # Restore original (cleanup)
    BaseModel.set_db_path(original_path)


@pytest.fixture
def controller(setup_test_db):
    """Provide a fresh EmployeeController instance."""
    from src.controllers.employee_controller import EmployeeController

    return EmployeeController()


@pytest.fixture
def sample_employee_data():
    """Provide valid sample employee data for testing."""
    return {
        "employee_id": "E999",
        "first_name": "Test",
        "last_name": "Employee",
        "surname": None,
        "date_of_birth": "1990-05-15",
        "gender": "Male",
        "status": "Active",
        "salary_type": "Salary",
        "job_title_name": "Software Engineer",
        "department_name": "Engineering",
        "email": "test.employee@abc.com",
        "has_picture": 0,
        "picture_filename": None,
        "address_line1": "123 Test Street",
        "address_line2": None,
        "city": "Test City",
        "state": "TS",
        "zip_code": "12345",
        "date_hired": "2024-01-15",
        "medical_type": "Single",
        "base_salary": 1500.00,
        "hourly_rate": None,
        "num_dependents": 0,
        "pto_balance": 0.0,
    }


@pytest.fixture
def invalid_employee_data():
    """Provide invalid employee data for validation testing."""
    return {
        "employee_id": "E998",
        "first_name": "Too",
        "last_name": "Young",
        "surname": None,
        "date_of_birth": "2020-01-01",  # Too young - under 18
        "gender": "Male",
        "status": "Active",
        "salary_type": "Salary",
        "job_title_name": "Test",
        "department_name": "Test",
        "email": "test@abc.com",
        "address_line1": "123 Test Street",
        "city": "Test City",
        "state": "TS",
        "zip_code": "12345",
        "date_hired": "2024-01-15",
    }
