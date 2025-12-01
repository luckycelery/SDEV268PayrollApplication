"""
Employee Routes - Employee self-service functionality

Handles:
- Employee dashboard
- Time entry
- Paycheck viewing
"""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from src.controllers.employee_controller import EmployeeController
from src.controllers.payroll_controller import PayrollController

bp = Blueprint("employee", __name__)

# Initialize controllers
employee_controller = EmployeeController()
payroll_controller = PayrollController()


def login_required(f):
    """Decorator to require user login."""
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to access this page.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


@bp.route("/")
@bp.route("/dashboard")
@login_required
def dashboard():
    """Employee dashboard - overview of their information."""
    # TODO: Get actual employee ID from session (linked via user account)
    # For now, show a placeholder
    employee_id = session.get("employee_id")

    if employee_id:
        success, message, employee = employee_controller.get_employee(employee_id)
        if success:
            return render_template("employee/dashboard.html", employee=employee)

    return render_template("employee/dashboard.html", employee=None)


@bp.route("/time-entry", methods=["GET", "POST"])
@login_required
def time_entry():
    """Time entry form for employees."""
    employee_id = session.get("employee_id")

    # Get current pay period
    start_date, end_date = payroll_controller.get_current_period()

    if request.method == "POST":
        entry_date = request.form.get("entry_date", "")
        hours_worked = float(request.form.get("hours_worked") or 0)
        pto_hours = float(request.form.get("pto_hours") or 0)
        notes = request.form.get("notes", "").strip() or None

        if employee_id:
            success, message, entry = payroll_controller.submit_time_entry(
                employee_id=employee_id,
                entry_date=entry_date,
                hours_worked=hours_worked,
                pto_hours=pto_hours,
                notes=notes,
            )

            if success:
                flash(message, "success")
            else:
                flash(message, "error")

    # Get existing entries for current period
    entries = []
    if employee_id:
        success, message, entries = payroll_controller.get_time_entries(
            employee_id, start_date, end_date
        )

    return render_template(
        "employee/time_entry.html",
        entries=entries,
        start_date=start_date,
        end_date=end_date,
    )


@bp.route("/paycheck")
@login_required
def paycheck():
    """View employee's paycheck history."""
    employee_id = session.get("employee_id")

    history = []
    if employee_id:
        success, message, history = payroll_controller.get_payroll_history(employee_id, limit=10)

    return render_template("employee/paycheck.html", payroll_history=history)
