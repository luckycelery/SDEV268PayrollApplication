# Employee Controller API Reference

> Quick reference for `EmployeeController` methods. See code docstrings for details.

## Return Pattern

Most methods return: `(success: bool, message: str, data)`

```python
success, message, employee = controller.get_employee("E001")
if success:
    print(employee.first_name)
else:
    flash(message, "error")
```

---

## Methods

| Method | Purpose | Returns |
|--------|---------|---------|
| `create_employee(data)` | Create new employee | `(bool, str, Employee\|None)` |
| `generate_employee_id()` | Get next available ID | `str` |
| `get_employee(id)` | Get employee by ID | `(bool, str, Employee\|None)` |
| `get_all_employees(include_terminated=False)` | List employees | `(bool, str, list[Employee])` |
| `search_employees(term)` | Search by name/email/ID | `(bool, str, list[Employee])` |
| `get_employees_by_department(dept)` | Filter by department | `(bool, str, list[Employee])` |
| `get_employee_summary(id)` | Get display-ready dict | `(bool, str, dict\|None)` |
| `update_employee(id, data)` | Update fields | `(bool, str, Employee\|None)` |
| `terminate_employee(id)` | Soft-delete | `(bool, str)` |
| `reactivate_employee(id)` | Restore terminated | `(bool, str)` |
| `delete_employee_permanently(id, confirm=True)` | Hard-delete ⚠️ | `(bool, str)` |
| `validate_employee_data(data)` | Validate without saving | `(bool, list[str])` |
| `get_employee_statistics()` | Workforce stats | `dict` |
| `get_departments_list()` | All departments | `list[str]` |
| `get_job_titles_list()` | All job titles | `list[str]` |

---

## Employee Fields

### Required Fields

| Field | Type | Notes |
|-------|------|-------|
| `employee_id` | str | Auto-generate with `generate_employee_id()` |
| `first_name` | str | |
| `last_name` | str | |
| `date_of_birth` | str | YYYY-MM-DD, must be 18+ |
| `gender` | str | "Male" or "Female" |
| `email` | str | Must be unique |
| `address_line1` | str | |
| `city` | str | |
| `state` | str | 2-letter abbreviation |
| `zip_code` | str | |
| `date_hired` | str | YYYY-MM-DD |
| `department_name` | str | Must exist in database |
| `job_title_name` | str | Must exist in database |

### Optional Fields

| Field | Type | Default |
|-------|------|---------|
| `surname` | str | None (suffix like Jr., Sr.) |
| `phone_num` | str | None |
| `address_line2` | str | None |
| `status` | str | "Active" |
| `salary_type` | str | None ("Salary" or "Hourly") |
| `base_salary` | float | None (annual, for salaried) |
| `hourly_rate` | float | None (for hourly) |
| `medical_type` | str | None ("Single" or "Family") |
| `num_dependents` | int | 0 |

---

## Employee Object

### Key Properties

```python
employee.employee_id      # "E001"
employee.first_name       # "John"
employee.last_name        # "Smith"
employee.email            # "john.smith@company.com"
employee.department_name  # "Engineering"
employee.job_title_name   # "Software Developer"
employee.status           # "Active" or "Terminated"
employee.salary_type      # "Salary" or "Hourly"
employee.base_salary      # 75000.00 (annual)
employee.hourly_rate      # 25.00
employee.pto_balance      # Available PTO hours
```

### Helper Methods

```python
employee.get_full_name()   # "John Smith Jr."
employee.calculate_age()   # 35
employee.is_active()       # True
employee.is_salaried()     # True
employee.get_pay_rate()    # "$1,442.31/week" or "$25.00/hour"
employee.to_dict()         # All fields as dict
```

---

## Common Patterns

### Create Employee

```python
data = {
    "employee_id": controller.generate_employee_id(),
    "first_name": "Jane",
    "last_name": "Doe",
    # ... other required fields
}
success, message, employee = controller.create_employee(data)
```

### Update Employee

```python
success, message, employee = controller.update_employee("E001", {
    "job_title_name": "Senior Developer",
    "base_salary": 85000.00
})
```

### Validate Before Save

```python
is_valid, errors = controller.validate_employee_data(form_data)
if not is_valid:
    for error in errors:
        flash(error, "error")
```
