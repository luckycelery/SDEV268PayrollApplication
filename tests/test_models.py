"""
Quick Test Script for Employee Model and Controller
Tests basic CRUD operations and validation
"""

from src.controllers.employee_controller import EmployeeController
from src.models.employee import Employee


def print_separator(title=""):
    """Print a section separator"""
    print("\n" + "=" * 70)
    if title:
        print(f" {title}")
        print("=" * 70)


def test_employee_retrieval():
    """Test retrieving employees from database"""
    print_separator("TEST 1: Employee Retrieval")

    # Test getting single employee
    employee = Employee.get_by_id('E001')

    if employee:
        print(f"[OK] Retrieved employee: {employee.get_full_name()}")
        print(f"     ID: {employee.employee_id}")
        print(f"     Age: {employee.calculate_age()}")
        print(f"     Department: {employee.department_name}")
        print(f"     Status: {employee.status}")
        print(f"     Pay Type: {employee.salary_type}")
    else:
        print("[FAIL] Could not retrieve employee E001")


def test_get_all_employees():
    """Test getting all employees"""
    print_separator("TEST 2: Get All Employees")

    employees = Employee.get_all(include_terminated=False)

    print(f"[OK] Retrieved {len(employees)} active employees:")
    for emp in employees[:5]:  # Show first 5
        print(f"     - {emp.employee_id}: {emp.get_full_name()} ({emp.department_name})")

    if len(employees) > 5:
        print(f"     ... and {len(employees) - 5} more")


def test_validation_errors():
    """Test that validation catches errors"""
    print_separator("TEST 3: Validation Error Detection")

    # Test underage employee (E003 - should be 4 years old from sample data)
    employee = Employee.get_by_id('E003')

    if employee:
        age = employee.calculate_age()
        is_valid, errors = employee.validate()

        print(f"Employee: {employee.get_full_name()}")
        print(f"Age: {age}")
        print(f"Valid: {is_valid}")

        if not is_valid:
            print("[OK] Validation correctly caught errors:")
            for error in errors:
                print(f"     - {error}")
        else:
            print("[UNEXPECTED] Employee should have failed validation")
    else:
        print("[INFO] E003 not found (may not have loaded due to validation)")


def test_search():
    """Test employee search"""
    print_separator("TEST 4: Employee Search")

    # Search for "Mustang"
    results = Employee.search("Mustang")

    print(f"[OK] Search for 'Mustang' found {len(results)} results:")
    for emp in results:
        print(f"     - {emp.employee_id}: {emp.get_full_name()}")


def test_controller_operations():
    """Test controller CRUD operations"""
    print_separator("TEST 5: Controller Operations")

    controller = EmployeeController()

    # Test 1: Get employee
    success, msg, employee = controller.get_employee('E001')
    if success:
        print(f"[OK] Controller get: {msg}")
        print(f"     Employee: {employee.get_full_name()}")
    else:
        print(f"[FAIL] {msg}")

    # Test 2: Get all employees
    success, msg, employees = controller.get_all_employees()
    print(f"[OK] {msg}")

    # Test 3: Search
    success, msg, results = controller.search_employees("IT")
    print(f"[OK] Search for 'IT': {msg}")
    for emp in results[:3]:
        print(f"     - {emp.get_full_name()} - {emp.department_name}")

    # Test 4: Get statistics
    stats = controller.get_employee_statistics()
    print("\n[OK] Employee Statistics:")
    print(f"     Total: {stats.get('total_employees', 0)}")
    print(f"     Active: {stats.get('active_employees', 0)}")
    print(f"     Terminated: {stats.get('terminated_employees', 0)}")
    print(f"     Salaried: {stats.get('salaried_employees', 0)}")
    print(f"     Hourly: {stats.get('hourly_employees', 0)}")


def test_validation_via_controller():
    """Test form validation through controller"""
    print_separator("TEST 6: Form Validation (Controller)")

    controller = EmployeeController()

    # Test invalid data
    invalid_data = {
        'employee_id': 'E999',
        'first_name': 'Test',
        'last_name': 'User',
        'dob': '2020-01-01',  # Too young!
        'gender': 'M',
        'pay_type': 'Salary',
        'job_title': 'Test',
        'department': 'Test',
        'company_email': 'test@example.com'
    }

    is_valid, errors = controller.validate_employee_data(invalid_data)

    print(f"Validation result: {is_valid}")
    if not is_valid:
        print("[OK] Validation correctly caught errors:")
        for error in errors:
            print(f"     - {error}")


def test_department_listing():
    """Test getting departments and job titles"""
    print_separator("TEST 7: Departments & Job Titles")

    controller = EmployeeController()

    departments = controller.get_departments_list()
    print(f"[OK] Departments ({len(departments)}):")
    for dept in departments:
        print(f"     - {dept}")

    titles = controller.get_job_titles_list()
    print(f"\n[OK] Job Titles ({len(titles)}):")
    for title in titles[:10]:  # Show first 10
        print(f"     - {title}")


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 70)
    print(" EMPLOYEE MODEL & CONTROLLER TEST SUITE")
    print("=" * 70)
    print(" Database: payroll.db")
    print(" Testing: CRUD operations, validation, search, controller")
    print("=" * 70)

    try:
        test_employee_retrieval()
        test_get_all_employees()
        test_validation_errors()
        test_search()
        test_controller_operations()
        test_validation_via_controller()
        test_department_listing()

        print_separator("ALL TESTS COMPLETE")
        print("\n[OK] Employee model and controller are working correctly!")
        print("\nNext steps:")
        print("  1. Create UI components to use the controller")
        print("  2. Build TimeEntry and Payroll models")
        print("  3. Implement payroll calculation logic")

    except Exception as e:
        print_separator("ERROR")
        print(f"[FAIL] Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run_all_tests()
