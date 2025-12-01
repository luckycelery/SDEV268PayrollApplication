# Flask Routes Reference

> **For Developers** - This document describes all Flask routes available in the payroll system web application.

## Overview

The application uses Flask Blueprints to organize routes by feature:

| Blueprint | URL Prefix | Purpose |
|-----------|------------|---------|
| `auth` | `/auth` | Login/logout |
| `admin` | `/admin` | Admin-only employee & system management |
| `employee` | `/employee` | Employee self-service |
| `payroll` | `/payroll` | Payroll management (admin) |

## Quick Reference

### Authentication Routes (`/auth`)

| Method | URL | Function | Auth Required |
|--------|-----|----------|---------------|
| GET/POST | `/auth/login` | `login()` | No |
| GET | `/auth/logout` | `logout()` | No |

### Admin Routes (`/admin`)

| Method | URL | Function | Auth Required |
|--------|-----|----------|---------------|
| GET | `/admin/` | `dashboard()` | Admin |
| GET | `/admin/dashboard` | `dashboard()` | Admin |
| GET | `/admin/employees` | `employee_list()` | Admin |
| GET/POST | `/admin/employees/add` | `employee_add()` | Admin |
| GET/POST | `/admin/employees/<id>/edit` | `employee_edit()` | Admin |
| POST | `/admin/employees/<id>/delete` | `employee_delete()` | Admin |

### Employee Routes (`/employee`)

| Method | URL | Function | Auth Required |
|--------|-----|----------|---------------|
| GET | `/employee/` | `dashboard()` | User |
| GET | `/employee/dashboard` | `dashboard()` | User |
| GET/POST | `/employee/time-entry` | `time_entry()` | User |
| GET | `/employee/paycheck` | `paycheck()` | User |

### Payroll Routes (`/payroll`)

| Method | URL | Function | Auth Required |
|--------|-----|----------|---------------|
| GET | `/payroll/` | `payroll_list()` | Admin |
| GET | `/payroll/current` | `current_period()` | Admin |
| POST | `/payroll/calculate` | `calculate_payroll()` | Admin |
| POST | `/payroll/approve/<id>` | `approve_payroll()` | Admin |
| GET | `/payroll/report/<id>` | `payroll_report()` | Admin |

---

## Authentication Routes

### `POST /auth/login`

Authenticate user and create session.

**Form Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | Yes | Username (case-insensitive) |
| `password` | string | Yes | Password |

**Behavior:**
- Admin users redirect to `/admin/dashboard`
- Employee users redirect to `/employee/dashboard`
- Failed login re-displays form with error flash

**Session Data Set:**
```python
session["user_id"]      # Employee ID or username
session["username"]     # Login username
session["user_type"]    # "Admin" or "Employee"
session["employee_id"]  # Employee ID (if applicable)
```

### `GET /auth/logout`

Clear session and redirect to login.

---

## Admin Routes

### `GET /admin/dashboard`

Admin overview page showing system statistics.

**Template:** `admin/dashboard.html`

**Context:**
```python
{
    "employee_count": int  # Total active employees
}
```

### `GET /admin/employees`

List all employees with optional search.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `search` | string | Filter by name, email, or ID |

**Template:** `admin/employee_list.html`

**Context:**
```python
{
    "employees": list[Employee],
    "search_term": str
}
```

### `GET/POST /admin/employees/add`

Create a new employee.

**Form Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `first_name` | string | Yes | First name |
| `last_name` | string | Yes | Last name |
| `surname` | string | No | Suffix (Jr., Sr., etc.) |
| `date_of_birth` | date | Yes | YYYY-MM-DD format |
| `gender` | string | Yes | "Male" or "Female" |
| `email` | string | Yes | Company email |
| `phone_num` | string | No | Phone number |
| `address_line1` | string | Yes | Street address |
| `address_line2` | string | No | Apt/Suite |
| `city` | string | Yes | City |
| `state` | string | Yes | State abbreviation |
| `zip_code` | string | Yes | ZIP code |
| `date_hired` | date | Yes | YYYY-MM-DD format |
| `department_name` | string | Yes | Department |
| `job_title_name` | string | Yes | Job title |
| `salary_type` | string | Yes | "Salary" or "Hourly" |
| `base_salary` | float | If salaried | Annual salary |
| `hourly_rate` | float | If hourly | Hourly rate |
| `medical_type` | string | No | "Single" or "Family" |
| `num_dependents` | int | No | Number of dependents |

**Template:** `admin/employee_form.html`

**Context:**
```python
{
    "employee": None,
    "departments": list[str],
    "action": "add"
}
```

**Success:** Redirect to `/admin/employees` with success flash

### `GET/POST /admin/employees/<employee_id>/edit`

Edit an existing employee.

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `employee_id` | string | Employee ID (e.g., "E001") |

**Form Fields:** Same as add, plus:

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | "Active" or "Terminated" |

**Template:** `admin/employee_form.html`

**Context:**
```python
{
    "employee": Employee,
    "departments": list[str],
    "action": "edit"
}
```

### `POST /admin/employees/<employee_id>/delete`

Terminate (soft-delete) an employee.

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `employee_id` | string | Employee ID |

**Behavior:** Sets employee status to "Terminated", redirects to employee list.

---

## Employee Routes

### `GET /employee/dashboard`

Employee's personal dashboard.

**Template:** `employee/dashboard.html`

**Context:**
```python
{
    "employee": Employee | None
}
```

### `GET/POST /employee/time-entry`

Submit and view time entries.

**Form Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `entry_date` | date | Yes | Date of work |
| `hours_worked` | float | Yes | Hours worked |
| `pto_hours` | float | No | PTO hours used |
| `notes` | string | No | Optional notes |

**Template:** `employee/time_entry.html`

**Context:**
```python
{
    "entries": list[TimeEntry],
    "start_date": str,  # Current period start
    "end_date": str     # Current period end
}
```

### `GET /employee/paycheck`

View paycheck history.

**Template:** `employee/paycheck.html`

**Context:**
```python
{
    "payroll_history": list[PayrollDetail]  # Last 10 paychecks
}
```

---

## Payroll Routes

### `GET /payroll/`

List all payroll periods.

**Template:** `payroll/payroll_list.html`

**Context:**
```python
{
    "periods": list[PayrollPeriod]
}
```

### `GET /payroll/current`

View current pay period details.

**Template:** `payroll/payroll_detail.html`

**Context:**
```python
{
    "period": PayrollPeriod,
    "details": list[PayrollDetail],
    "start_date": str,
    "end_date": str
}
```

### `POST /payroll/calculate`

Calculate payroll for current period.

**Behavior:**
- Calculates pay for all active employees
- Creates/updates PayrollDetail records
- Redirects to `/payroll/current` with flash message

### `POST /payroll/approve/<payroll_id>`

Approve and lock a payroll period.

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `payroll_id` | int | Payroll period ID |

**Behavior:**
- Sets `is_locked = 1` on PayrollPeriod
- Records `processed_by` as current admin
- Prevents future edits to time entries

### `GET /payroll/report/<payroll_id>`

Generate detailed payroll report.

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `payroll_id` | int | Payroll period ID |

**Template:** `payroll/payroll_report.html`

**Context:**
```python
{
    "period": PayrollPeriod,
    "summary": dict,         # Aggregate totals
    "details": list[PayrollDetail]
}
```

---

## Access Control

### Decorators

Two decorators are used for access control:

```python
@admin_required    # Requires user_type == "Admin"
@login_required    # Requires any authenticated user
```

### Unauthorized Access

- No session: Redirect to `/auth/login` with "Please log in" flash
- Non-admin accessing admin route: Redirect with "Admin access required" flash

---

## Flash Message Categories

Flash messages use Bootstrap alert classes:

| Category | CSS Class | Usage |
|----------|-----------|-------|
| `success` | `alert-success` | Action completed successfully |
| `error` | `alert-danger` | Action failed |
| `info` | `alert-info` | Informational message |

**Example in template:**
```html
{% for category, message in get_flashed_messages(with_categories=true) %}
    <div class="alert alert-{{ category }}">{{ message }}</div>
{% endfor %}
```

---

## Running the Application

```bash
# With UV
uv run flask run
# Or
uv run python app.py

# Without UV (activate venv first)
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux
python app.py

# Access at http://127.0.0.1:5000
```

**Default Login examples:**
- Admin: `HR0001` / `AbccoTeam3`
- Employee: `roy.mustang` / `roy.mustang11062005`

---

*Last Updated: December 1, 2025*
