"""
Admin Routes - Admin-only functionality

Handles:
- Admin dashboard
- Employee management (list, add, edit, delete)
- Employee search
"""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from src.controllers.employee_controller import EmployeeController
from src.models.base_model import BaseModel

bp = Blueprint("admin", __name__)


def get_departments() -> list[str]:
    """Fetch all department names from the database."""
    rows = BaseModel.execute_query(
        "SELECT department_name FROM departments ORDER BY department_name"
    )
    return [row["department_name"] for row in rows]


# Initialize controller
employee_controller = EmployeeController()


def admin_required(f):
    """Decorator to require admin login."""
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to access this page.", "error")
            return redirect(url_for("auth.login"))
        if session.get("user_type") != "Admin":
            flash("Admin access required.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


@bp.route("/")
@bp.route("/dashboard")
@admin_required
def dashboard():
    """Admin dashboard - overview of system status."""
    # Get summary statistics
    success, message, employees = employee_controller.get_all_employees()
    employee_count = len(employees) if success else 0

    return render_template(
        "admin/dashboard.html",
        employee_count=employee_count,
    )


@bp.route("/employees")
@admin_required
def employee_list():
    """List all employees with search functionality."""
    search_term = request.args.get("search", "").strip()

    if search_term:
        success, message, employees = employee_controller.search_employees(search_term)
    else:
        success, message, employees = employee_controller.get_all_employees()

    return render_template(
        "admin/employee_list.html",
        employees=employees,
        search_term=search_term,
    )


@bp.route("/employees/add", methods=["GET", "POST"])
@admin_required
def employee_add():
    """Add a new employee."""
    if request.method == "POST":
        # Collect form data
        employee_data = {
            "employee_id": employee_controller.generate_employee_id(),
            "first_name": request.form.get("first_name", "").strip(),
            "last_name": request.form.get("last_name", "").strip(),
            "surname": request.form.get("surname", "").strip() or None,
            "date_of_birth": request.form.get("date_of_birth", ""),
            "gender": request.form.get("gender", ""),
            "email": request.form.get("email", "").strip(),
            "phone_num": request.form.get("phone_num", "").strip() or None,
            "address_line1": request.form.get("address_line1", "").strip(),
            "address_line2": request.form.get("address_line2", "").strip() or None,
            "city": request.form.get("city", "").strip(),
            "state": request.form.get("state", "").strip().upper(),
            "zip_code": request.form.get("zip_code", "").strip(),
            "date_hired": request.form.get("date_hired", ""),
            "department_name": request.form.get("department_name", ""),
            "job_title_name": request.form.get("job_title_name", ""),
            "salary_type": request.form.get("salary_type", ""),
            "base_salary": float(request.form.get("base_salary") or 0) or None,
            "hourly_rate": float(request.form.get("hourly_rate") or 0) or None,
            "medical_type": request.form.get("medical_type", "Single"),
            "num_dependents": int(request.form.get("num_dependents") or 0),
        }

        success, message, employee = employee_controller.create_employee(employee_data)

        if success:
            flash(message, "success")
            return redirect(url_for("admin.employee_list"))
        else:
            flash(message, "error")

    return render_template(
        "admin/employee_form.html",
        employee=None,
        departments=get_departments(),
        action="add",
    )


@bp.route("/employees/<employee_id>/edit", methods=["GET", "POST"])
@admin_required
def employee_edit(employee_id):
    """Edit an existing employee."""
    success, message, employee = employee_controller.get_employee(employee_id)

    if not success:
        flash(message, "error")
        return redirect(url_for("admin.employee_list"))

    if request.method == "POST":
        # Collect updated form data
        update_data = {
            "first_name": request.form.get("first_name", "").strip(),
            "last_name": request.form.get("last_name", "").strip(),
            "surname": request.form.get("surname", "").strip() or None,
            "date_of_birth": request.form.get("date_of_birth", ""),
            "gender": request.form.get("gender", ""),
            "email": request.form.get("email", "").strip(),
            "phone_num": request.form.get("phone_num", "").strip() or None,
            "address_line1": request.form.get("address_line1", "").strip(),
            "address_line2": request.form.get("address_line2", "").strip() or None,
            "city": request.form.get("city", "").strip(),
            "state": request.form.get("state", "").strip().upper(),
            "zip_code": request.form.get("zip_code", "").strip(),
            "department_name": request.form.get("department_name", ""),
            "job_title_name": request.form.get("job_title_name", ""),
            "status": request.form.get("status", "Active"),
        }

        success, message, _ = employee_controller.update_employee(employee_id, update_data)

        if success:
            flash(message, "success")
            return redirect(url_for("admin.employee_list"))
        else:
            flash(message, "error")

    return render_template(
        "admin/employee_form.html",
        employee=employee,
        departments=get_departments(),
        action="edit",
    )


@bp.route("/employees/<employee_id>/delete", methods=["POST"])
@admin_required
def employee_delete(employee_id):
    """Delete (terminate) an employee."""
    success, message = employee_controller.terminate_employee(employee_id)

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect(url_for("admin.employee_list"))
