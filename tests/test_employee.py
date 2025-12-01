"""
Employee Model and Controller Tests
Tests CRUD operations, validation, and business logic.

Run with: uv run pytest tests/test_employee.py -v
"""


from src.models.employee import Employee


class TestEmployeeModel:
    """Tests for the Employee model."""

    def test_get_employee_by_id(self):
        """Test retrieving a single employee by ID."""
        employee = Employee.get_by_id("E001")

        assert employee is not None
        assert employee.employee_id == "E001"
        assert employee.first_name is not None
        assert employee.last_name is not None

    def test_get_employee_not_found(self):
        """Test retrieving non-existent employee returns None."""
        employee = Employee.get_by_id("ENOTEXIST")

        assert employee is None

    def test_get_all_employees_active_only(self):
        """Test retrieving only active employees."""
        employees = Employee.get_all(include_terminated=False)

        assert len(employees) > 0
        assert all(emp.status == "Active" for emp in employees)

    def test_get_all_employees_including_terminated(self):
        """Test retrieving all employees including terminated."""
        all_employees = Employee.get_all(include_terminated=True)
        active_only = Employee.get_all(include_terminated=False)

        assert len(all_employees) >= len(active_only)

    def test_employee_full_name(self):
        """Test full name generation."""
        employee = Employee.get_by_id("E001")

        assert employee is not None
        full_name = employee.get_full_name()
        assert employee.first_name in full_name
        assert employee.last_name in full_name

    def test_employee_age_calculation(self):
        """Test age calculation from DOB."""
        employee = Employee.get_by_id("E001")

        assert employee is not None
        age = employee.calculate_age()
        assert isinstance(age, int)
        assert age > 0

    def test_employee_is_active(self):
        """Test is_active helper method."""
        employee = Employee.get_by_id("E001")

        assert employee is not None
        assert employee.is_active() == (employee.status == "Active")

    def test_employee_is_salaried(self):
        """Test is_salaried helper method."""
        employee = Employee.get_by_id("E001")

        assert employee is not None
        assert employee.is_salaried() == (employee.salary_type == "Salary")

    def test_search_employees(self):
        """Test employee search functionality."""
        # Search should return results for common terms
        results = Employee.search("E00")

        assert isinstance(results, list)
        # All results should have the search term in ID, name, or email
        for emp in results:
            searchable = f"{emp.employee_id} {emp.first_name} {emp.last_name} {emp.email}".lower()
            assert "e00" in searchable

    def test_get_by_department(self):
        """Test getting employees by department."""
        # First get a valid department
        all_employees = Employee.get_all()
        if all_employees:
            dept = all_employees[0].department_name
            dept_employees = Employee.get_by_department(dept)

            assert len(dept_employees) > 0
            assert all(emp.department_name == dept for emp in dept_employees)

    def test_employee_to_dict(self):
        """Test employee to dictionary conversion."""
        employee = Employee.get_by_id("E001")

        assert employee is not None
        data = employee.to_dict()

        assert isinstance(data, dict)
        assert data["employee_id"] == "E001"
        assert "full_name" in data
        assert "age" in data


class TestEmployeeValidation:
    """Tests for employee validation logic."""

    def test_valid_employee_passes_validation(self, sample_employee_data):
        """Test that valid employee data passes validation."""
        employee = Employee(**sample_employee_data)
        is_valid, errors = employee.validate()

        assert is_valid is True
        assert len(errors) == 0

    def test_underage_employee_fails_validation(self, invalid_employee_data):
        """Test that underage employee fails validation."""
        employee = Employee(**invalid_employee_data)
        is_valid, errors = employee.validate()

        assert is_valid is False
        assert any("18" in error for error in errors)

    def test_missing_required_fields(self):
        """Test that missing required fields cause validation failure."""
        employee = Employee(
            employee_id="",  # Empty - should fail
            first_name="Test",
            last_name="User",
            surname=None,
            date_of_birth="1990-01-01",
            gender="Male",
            status="Active",
            salary_type="Salary",
            job_title_name="Test",
            department_name="Test",
            email="test@abc.com",
            address_line1="123 Test Street",
            city="Test City",
            state="TS",
            zip_code="12345",
            date_hired="2024-01-15",
        )

        is_valid, errors = employee.validate()

        assert is_valid is False
        assert any("Employee ID" in error for error in errors)

    def test_invalid_email_format(self):
        """Test that invalid email format fails validation."""
        employee = Employee(
            employee_id="E999",
            first_name="Test",
            last_name="User",
            date_of_birth="1990-01-01",
            gender="Male",
            status="Active",
            salary_type="Salary",
            job_title_name="Test",
            department_name="Test",
            email="invalid-email",  # No @ symbol
            address_line1="123 Test Street",
            city="Test City",
            state="TS",
            zip_code="12345",
            date_hired="2024-01-15",
        )

        is_valid, errors = employee.validate()

        assert is_valid is False
        assert any("email" in error.lower() for error in errors)

    def test_invalid_gender(self):
        """Test that invalid gender fails validation."""
        employee = Employee(
            employee_id="E999",
            first_name="Test",
            last_name="User",
            date_of_birth="1990-01-01",
            gender="X",  # Invalid - not Male or Female
            status="Active",
            salary_type="Salary",
            job_title_name="Test",
            department_name="Test",
            email="test@abc.com",
            address_line1="123 Test Street",
            city="Test City",
            state="TS",
            zip_code="12345",
            date_hired="2024-01-15",
        )

        is_valid, errors = employee.validate()

        assert is_valid is False
        assert any("Gender" in error for error in errors)

    def test_negative_salary_fails(self):
        """Test that negative salary fails validation."""
        employee = Employee(
            employee_id="E999",
            first_name="Test",
            last_name="User",
            date_of_birth="1990-01-01",
            gender="Male",
            status="Active",
            salary_type="Salary",
            job_title_name="Test",
            department_name="Test",
            email="test@abc.com",
            address_line1="123 Test Street",
            city="Test City",
            state="TS",
            zip_code="12345",
            date_hired="2024-01-15",
            base_salary=-100.00,  # Negative
        )

        is_valid, errors = employee.validate()

        assert is_valid is False
        assert any("salary" in error.lower() for error in errors)


class TestEmployeeController:
    """Tests for the EmployeeController."""

    def test_get_employee_success(self, controller):
        """Test successful employee retrieval via controller."""
        success, message, employee = controller.get_employee("E001")

        assert success is True
        assert employee is not None
        assert employee.employee_id == "E001"

    def test_get_employee_not_found(self, controller):
        """Test employee not found via controller."""
        success, message, employee = controller.get_employee("ENOTEXIST")

        assert success is False
        assert employee is None
        assert "not found" in message.lower()

    def test_get_all_employees(self, controller):
        """Test getting all employees via controller."""
        success, message, employees = controller.get_all_employees()

        assert success is True
        assert isinstance(employees, list)
        assert len(employees) > 0

    def test_search_employees(self, controller):
        """Test employee search via controller."""
        success, message, results = controller.search_employees("E00")

        assert success is True
        assert isinstance(results, list)

    def test_search_empty_term_fails(self, controller):
        """Test that empty search term fails."""
        success, message, results = controller.search_employees("")

        assert success is False
        assert len(results) == 0

    def test_get_employee_summary(self, controller):
        """Test getting employee summary."""
        success, message, summary = controller.get_employee_summary("E001")

        assert success is True
        assert summary is not None
        assert "id" in summary
        assert "name" in summary
        assert "age" in summary

    def test_validate_employee_data(self, controller, sample_employee_data):
        """Test validation via controller."""
        is_valid, errors = controller.validate_employee_data(sample_employee_data)

        assert is_valid is True
        assert len(errors) == 0

    def test_validate_invalid_data(self, controller, invalid_employee_data):
        """Test validation catches errors via controller."""
        is_valid, errors = controller.validate_employee_data(invalid_employee_data)

        assert is_valid is False
        assert len(errors) > 0

    def test_get_employee_statistics(self, controller):
        """Test getting employee statistics."""
        stats = controller.get_employee_statistics()

        assert isinstance(stats, dict)
        assert "total_employees" in stats
        assert "active_employees" in stats
        assert "departments" in stats

    def test_get_departments_list(self, controller):
        """Test getting list of departments."""
        departments = controller.get_departments_list()

        assert isinstance(departments, list)
        assert len(departments) > 0
        # Should be sorted
        assert departments == sorted(departments)

    def test_get_job_titles_list(self, controller):
        """Test getting list of job titles."""
        titles = controller.get_job_titles_list()

        assert isinstance(titles, list)
        assert len(titles) > 0
        # Should be sorted
        assert titles == sorted(titles)

    def test_generate_employee_id(self, controller):
        """Test generating next employee ID."""
        new_id = controller.generate_employee_id()

        assert new_id.startswith("E")
        assert len(new_id) == 4  # E + 3 digits
        assert new_id[1:].isdigit()


class TestEmployeeControllerCRUD:
    """Tests for Create, Update, Delete operations."""

    def test_create_employee(self, controller, sample_employee_data):
        """Test creating a new employee."""
        # Use a unique ID
        sample_employee_data["employee_id"] = controller.generate_employee_id()
        sample_employee_data["email"] = f"test{sample_employee_data['employee_id']}@abc.com"

        success, message, employee = controller.create_employee(sample_employee_data)

        assert success is True
        assert employee is not None
        assert employee.employee_id == sample_employee_data["employee_id"]

    def test_create_duplicate_employee_fails(self, controller, sample_employee_data):
        """Test that creating duplicate employee fails."""
        sample_employee_data["employee_id"] = "E001"  # Existing ID

        success, message, employee = controller.create_employee(sample_employee_data)

        assert success is False
        assert "exists" in message.lower()

    def test_update_employee(self, controller):
        """Test updating an employee."""
        success, message, employee = controller.update_employee(
            "E001", {"job_title_name": "Senior Test Engineer"}
        )

        assert success is True
        assert employee is not None

    def test_update_nonexistent_employee_fails(self, controller):
        """Test that updating non-existent employee fails."""
        success, message, employee = controller.update_employee(
            "ENOTEXIST", {"job_title_name": "Test"}
        )

        assert success is False
        assert employee is None

    def test_terminate_employee(self, controller, sample_employee_data):
        """Test terminating an employee."""
        # First create an employee to terminate
        sample_employee_data["employee_id"] = controller.generate_employee_id()
        sample_employee_data["email"] = f"term{sample_employee_data['employee_id']}@abc.com"
        controller.create_employee(sample_employee_data)

        success, message = controller.terminate_employee(sample_employee_data["employee_id"])

        assert success is True
        assert "terminated" in message.lower()

    def test_reactivate_employee(self, controller, sample_employee_data):
        """Test reactivating a terminated employee."""
        # Create and terminate an employee
        sample_employee_data["employee_id"] = controller.generate_employee_id()
        sample_employee_data["email"] = f"react{sample_employee_data['employee_id']}@abc.com"
        controller.create_employee(sample_employee_data)
        controller.terminate_employee(sample_employee_data["employee_id"])

        success, message = controller.reactivate_employee(sample_employee_data["employee_id"])

        assert success is True
