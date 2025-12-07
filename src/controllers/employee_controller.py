"""
Employee Controller - Business logic for employee management
Coordinates between UI and Employee model
Matches the updated Employee model based on database schema
"""

from src.models.employee import Employee
from src.utils.constants import (
    EMPLOYEE_STATUS_ACTIVE,
    EMPLOYEE_STATUS_TERMINATED,
)


class EmployeeController:
    """
    Controller for employee management operations

    Handles:
    - Creating, reading, updating, deleting employees
    - Validation and error handling
    - Search and filtering
    - Business logic coordination
    """

    def __init__(self):
        """Initialize employee controller."""
        pass

    # ==================== CREATE OPERATIONS ====================

    def create_employee(self, employee_data: dict) -> tuple[bool, str, Employee | None]:
        """
        Create a new employee with validation.

        Args:
            employee_data: Dictionary with employee information

        Returns:
            Tuple of (success, message, employee_object)
        """
        try:
            # Create employee object
            employee = Employee(
                employee_id=employee_data.get("employee_id", ""),
                first_name=employee_data.get("first_name", ""),
                last_name=employee_data.get("last_name", ""),
                surname=employee_data.get("surname"),
                date_of_birth=employee_data.get("date_of_birth", ""),
                gender=employee_data.get("gender", ""),
                email=employee_data.get("email", ""),
                phone_num=employee_data.get("phone_num"),
                address_line1=employee_data.get("address_line1", ""),
                address_line2=employee_data.get("address_line2"),
                city=employee_data.get("city", ""),
                state=employee_data.get("state", ""),
                zip_code=employee_data.get("zip_code", ""),
                has_picture=employee_data.get("has_picture", 0),
                picture_filename=employee_data.get("picture_filename"),
                status=employee_data.get("status", EMPLOYEE_STATUS_ACTIVE),
                date_hired=employee_data.get("date_hired", ""),
                department_name=employee_data.get("department_name", ""),
                job_title_name=employee_data.get("job_title_name", ""),
                # Compensation fields
                salary_type=employee_data.get("salary_type"),
                base_salary=employee_data.get("base_salary"),
                hourly_rate=employee_data.get("hourly_rate"),
                medical_type=employee_data.get("medical_type"),
                num_dependents=employee_data.get("num_dependents", 0),
            )

            # Validate before saving
            is_valid, errors = employee.validate()
            if not is_valid:
                error_msg = "Validation failed:\n" + "\n".join(f"- {err}" for err in errors)
                return False, error_msg, None

            # Check if employee ID already exists
            existing = Employee.get_by_id(employee.employee_id)
            if existing:
                return False, f"Employee ID {employee.employee_id} already exists", None

            # Save to database
            employee.save()

            return True, f"Employee {employee.first_name} {employee.last_name} created successfully", employee

        except Exception as e:
            return False, f"Error creating employee: {e!s}", None

    def generate_employee_id(self) -> str:
        """
        Generate next available employee ID.

        Returns:
            Next employee ID (e.g., 'E013')
        """
        all_employees = Employee.get_all(include_terminated=True)

        if not all_employees:
            return "E001"

        # Extract numeric part and find max
        max_id = 0
        for emp in all_employees:
            try:
                num = int(emp.employee_id[1:])  # Skip 'E' prefix
                if num > max_id:
                    max_id = num
            except (ValueError, IndexError):
                continue

        return f"E{(max_id + 1):03d}"

    # ==================== READ OPERATIONS ====================

    def get_employee(self, employee_id: str) -> tuple[bool, str, Employee | None]:
        """
        Retrieve employee by ID.

        Args:
            employee_id: Employee ID to retrieve

        Returns:
            Tuple of (success, message, employee_object)
        """
        try:
            employee = Employee.get_by_id(employee_id)

            if employee:
                return True, "Employee found", employee
            return False, f"Employee {employee_id} not found", None

        except Exception as e:
            return False, f"Error retrieving employee: {e!s}", None

    def get_all_employees(self, include_terminated: bool = False) -> tuple[bool, str, list[Employee]]:
        """
        Get all employees.

        Args:
            include_terminated: Include terminated employees

        Returns:
            Tuple of (success, message, list_of_employees)
        """
        try:
            employees = Employee.get_all(include_terminated=include_terminated)

            status = "active" if not include_terminated else "all"
            return True, f"Retrieved {len(employees)} {status} employees", employees

        except Exception as e:
            return False, f"Error retrieving employees: {e!s}", []

    def search_employees(self, search_term: str) -> tuple[bool, str, list[Employee]]:
        """
        Search employees by name, email, or ID.

        Args:
            search_term: Text to search for

        Returns:
            Tuple of (success, message, list_of_employees)
        """
        try:
            if not search_term or not search_term.strip():
                return False, "Search term cannot be empty", []

            employees = Employee.search(search_term.strip())

            return True, f"Found {len(employees)} matching employees", employees

        except Exception as e:
            return False, f"Error searching employees: {e!s}", []

    def get_employees_by_department(self, department: str) -> tuple[bool, str, list[Employee]]:
        """
        Get all employees in a department.

        Args:
            department: Department name

        Returns:
            Tuple of (success, message, list_of_employees)
        """
        try:
            employees = Employee.get_by_department(department)

            return True, f"Found {len(employees)} employees in {department}", employees

        except Exception as e:
            return False, f"Error retrieving department employees: {e!s}", []

    def get_employee_summary(self, employee_id: str) -> tuple[bool, str, dict | None]:
        """
        Get employee summary information for display.

        Args:
            employee_id: Employee ID

        Returns:
            Tuple of (success, message, summary_dict)
        """
        success, msg, employee = self.get_employee(employee_id)

        if not success or employee is None:
            return False, msg, None

        summary = {
            "id": employee.employee_id,
            "name": employee.get_full_name(),
            "age": employee.calculate_age(),
            "department": employee.department_name,
            "job_title": employee.job_title_name,
            "status": employee.status,
            "salary_type": employee.salary_type,
            "email": employee.email,
            "pay_rate": employee.get_pay_rate(),
            "is_active": employee.is_active(),
            "is_salaried": employee.is_salaried(),
        }

        return True, "Summary generated", summary

    # ==================== UPDATE OPERATIONS ====================

    def update_employee(self, employee_id: str, updated_data: dict) -> tuple[bool, str, Employee | None]:
        """
        Update existing employee.

        Args:
            employee_id: Employee ID to update
            updated_data: Dictionary with fields to update

        Returns:
            Tuple of (success, message, employee_object)
        """
        try:
            # Get existing employee
            employee = Employee.get_by_id(employee_id)

            if not employee:
                return False, f"Employee {employee_id} not found", None

            # Update core fields
            if "first_name" in updated_data:
                employee.first_name = updated_data["first_name"]
            if "last_name" in updated_data:
                employee.last_name = updated_data["last_name"]
            if "surname" in updated_data:
                employee.surname = updated_data["surname"]
            if "date_of_birth" in updated_data:
                employee.date_of_birth = updated_data["date_of_birth"]
            if "gender" in updated_data:
                employee.gender = updated_data["gender"]
            if "email" in updated_data:
                employee.email = updated_data["email"]
            if "phone_num" in updated_data:
                employee.phone_num = updated_data["phone_num"]
            if "status" in updated_data:
                employee.status = updated_data["status"]
            if "has_picture" in updated_data:
                employee.has_picture = updated_data["has_picture"]
            if "picture_filename" in updated_data:
                employee.picture_filename = updated_data["picture_filename"]

            # Address fields
            if "address_line1" in updated_data:
                employee.address_line1 = updated_data["address_line1"]
            if "address_line2" in updated_data:
                employee.address_line2 = updated_data["address_line2"]
            if "city" in updated_data:
                employee.city = updated_data["city"]
            if "state" in updated_data:
                employee.state = updated_data["state"]
            if "zip_code" in updated_data:
                employee.zip_code = updated_data["zip_code"]

            # Employment info
            if "date_hired" in updated_data:
                employee.date_hired = updated_data["date_hired"]
            if "department_name" in updated_data:
                employee.department_name = updated_data["department_name"]
            if "job_title_name" in updated_data:
                employee.job_title_name = updated_data["job_title_name"]

            # Compensation fields
            if "salary_type" in updated_data:
                employee.salary_type = updated_data["salary_type"]
            if "base_salary" in updated_data:
                employee.base_salary = updated_data["base_salary"]
            if "hourly_rate" in updated_data:
                employee.hourly_rate = updated_data["hourly_rate"]
            if "medical_type" in updated_data:
                employee.medical_type = updated_data["medical_type"]
            if "num_dependents" in updated_data:
                employee.num_dependents = updated_data["num_dependents"]

            # Validate updated data
            is_valid, errors = employee.validate()
            if not is_valid:
                error_msg = "Validation failed:\n" + "\n".join(f"- {err}" for err in errors)
                return False, error_msg, None

            # Save changes
            employee.save()

            return True, f"Employee {employee.first_name} {employee.last_name} updated successfully", employee

        except Exception as e:
            return False, f"Error updating employee: {e!s}", None

    def terminate_employee(self, employee_id: str) -> tuple[bool, str]:
        """
        Terminate an employee (soft delete).

        Args:
            employee_id: Employee ID to terminate

        Returns:
            Tuple of (success, message)
        """
        try:
            employee = Employee.get_by_id(employee_id)

            if not employee:
                return False, f"Employee {employee_id} not found"

            if employee.status == EMPLOYEE_STATUS_TERMINATED:
                return False, f"Employee {employee.get_full_name()} is already terminated"

            employee.delete()

            return True, f"Employee {employee.get_full_name()} terminated successfully"

        except Exception as e:
            return False, f"Error terminating employee: {e!s}"

    def reactivate_employee(self, employee_id: str) -> tuple[bool, str]:
        """
        Reactivate a terminated employee.

        Args:
            employee_id: Employee ID to reactivate

        Returns:
            Tuple of (success, message)
        """
        try:
            employee = Employee.get_by_id(employee_id)

            if not employee:
                return False, f"Employee {employee_id} not found"

            if employee.status == EMPLOYEE_STATUS_ACTIVE:
                return False, f"Employee {employee.get_full_name()} is already active"

            return self.update_employee(employee_id, {"status": EMPLOYEE_STATUS_ACTIVE})[:2]

        except Exception as e:
            return False, f"Error reactivating employee: {e!s}"

    # ==================== DELETE OPERATIONS ====================

    def delete_employee_permanently(self, employee_id: str, confirm: bool = False) -> tuple[bool, str]:
        """
        Permanently delete employee from database.
        WARNING: This cannot be undone!

        Args:
            employee_id: Employee ID to delete
            confirm: Must be True to proceed (safety check)

        Returns:
            Tuple of (success, message)
        """
        if not confirm:
            return False, "Deletion requires confirmation (set confirm=True)"

        try:
            employee = Employee.get_by_id(employee_id)

            if not employee:
                return False, f"Employee {employee_id} not found"

            employee_name = employee.get_full_name()
            Employee.hard_delete(employee_id)

            return True, f"Employee {employee_name} permanently deleted"

        except Exception as e:
            return False, f"Error deleting employee: {e!s}"

    # ==================== VALIDATION HELPERS ====================

    def validate_employee_data(self, employee_data: dict) -> tuple[bool, list[str]]:
        """
        Validate employee data without saving.
        Useful for form validation in UI.

        Args:
            employee_data: Dictionary with employee information

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        try:
            # Create temporary employee object for validation
            employee = Employee(
                employee_id=employee_data.get("employee_id", "TEMP"),
                first_name=employee_data.get("first_name", ""),
                last_name=employee_data.get("last_name", ""),
                surname=employee_data.get("surname"),
                phone_num=employee_data.get("phone_num"),
                date_of_birth=employee_data.get("date_of_birth", ""),
                gender=employee_data.get("gender", ""),
                email=employee_data.get("email", ""),
                address_line1=employee_data.get("address_line1", ""),
                address_line2=employee_data.get("address_line2"),
                city=employee_data.get("city", ""),
                state=employee_data.get("state", ""),
                zip_code=employee_data.get("zip_code", ""),
                status=employee_data.get("status", EMPLOYEE_STATUS_ACTIVE),
                date_hired=employee_data.get("date_hired", ""),
                department_name=employee_data.get("department_name", ""),
                job_title_name=employee_data.get("job_title_name", ""),
                salary_type=employee_data.get("salary_type"),
                base_salary=employee_data.get("base_salary"),
                hourly_rate=employee_data.get("hourly_rate"),
                medical_type=employee_data.get("medical_type"),
                num_dependents=employee_data.get("num_dependents", 0),
            )

            return employee.validate()

        except Exception as e:
            return False, [f"Validation error: {e!s}"]

    # ==================== REPORTING & STATISTICS ====================

    def get_employee_statistics(self) -> dict:
        """
        Get statistics about employees.

        Returns:
            Dictionary with statistics
        """
        try:
            all_employees = Employee.get_all(include_terminated=True)
            active_employees = [e for e in all_employees if e.is_active()]

            # Count by department
            departments: dict[str, int] = {}
            for emp in active_employees:
                dept = emp.department_name
                departments[dept] = departments.get(dept, 0) + 1

            # Count by pay type
            salaried = len([e for e in active_employees if e.is_salaried()])
            hourly = len(active_employees) - salaried

            return {
                "total_employees": len(all_employees),
                "active_employees": len(active_employees),
                "terminated_employees": len(all_employees) - len(active_employees),
                "salaried_employees": salaried,
                "hourly_employees": hourly,
                "departments": departments,
            }

        except Exception as e:
            return {"error": str(e)}

    def get_departments_list(self) -> list[str]:
        """
        Get list of unique departments.

        Returns:
            Sorted list of department names
        """
        try:
            employees = Employee.get_all(include_terminated=True)
            departments = {emp.department_name for emp in employees if emp.department_name}
            return sorted(departments)

        except Exception:
            return []

    def get_job_titles_list(self) -> list[str]:
        """
        Get list of unique job titles.

        Returns:
            Sorted list of job titles
        """
        try:
            employees = Employee.get_all(include_terminated=True)
            titles = {emp.job_title_name for emp in employees if emp.job_title_name}
            return sorted(titles)

        except Exception:
            return []
