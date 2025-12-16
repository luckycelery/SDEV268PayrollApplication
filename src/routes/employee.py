"""
Employee Routes - Employee self-service functionality

Handles:
- Employee dashboard
- Time entry
- Paycheck viewing
"""

from flask import Blueprint, flash, redirect, render_template, request, send_file, session, url_for

from src.controllers.employee_controller import EmployeeController
from src.controllers.payroll_controller import PayrollController
from src.models.payroll import PayrollDetail, PayrollPeriod
from src.utils.pdf_generator import generate_paycheck_pdf

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

    # Get employee for PTO balance and salary type
    pto_balance = 0.0
    employee = None
    salary_type = None
    if employee_id:
        success, message, employee = employee_controller.get_employee(employee_id)
        if success and employee:
            pto_balance = employee.pto_balance
            salary_type = employee.salary_type

    if request.method == "POST":
        entry_date = request.form.get("entry_date", "")
        hours_worked = float(request.form.get("hours_worked") or 0)
        pto_hours = float(request.form.get("pto_hours") or 0)
        notes = request.form.get("notes", "").strip() or None

        # Validate PTO hours against balance
        if pto_hours > pto_balance:
            flash(f"PTO hours ({pto_hours}) exceeds available balance ({pto_balance:.2f} hours).", "error")
        elif employee_id:
            success, message, entry = payroll_controller.submit_time_entry(
                employee_id=employee_id,
                entry_date=entry_date,
                hours_worked=hours_worked,
                pto_hours=pto_hours,
                notes=notes,
            )

            if success:
                flash(message, "success")
                # Refresh PTO balance after successful entry
                success, message, employee = employee_controller.get_employee(employee_id)
                if success and employee:
                    pto_balance = employee.pto_balance
            else:
                flash(message, "error")

    # Get existing entries for current period
    entries = []
    pay_preview = None
    if employee_id:
        success, message, entries = payroll_controller.get_time_entries(
            employee_id, start_date, end_date
        )

        # Always calculate pay preview (even with no entries, will show $0)
        success, message, pay_preview = payroll_controller.calculate_weekly_pay(
            employee_id, start_date, end_date
        )

    return render_template(
        "employee/time_entry.html",
        entries=entries,
        start_date=start_date,
        end_date=end_date,
        pto_balance=pto_balance,
        employee=employee,
        salary_type=salary_type,
        pay_preview=pay_preview,
    )


@bp.route("/payroll-history")
@login_required
def payroll_history():
    """View employee's payroll history."""
    employee_id = session.get("employee_id")

    history = []
    if employee_id:
        success, message, history = payroll_controller.get_payroll_history(employee_id, limit=10)

    return render_template("employee/payroll_history.html", payroll_history=history)


@bp.route("/paycheck/<int:payroll_detail_id>")
@login_required
def paycheck_detail(payroll_detail_id):
    """View detailed paycheck breakdown."""
    employee_id = session.get("employee_id")

    if not employee_id:
        flash("Employee ID not found.", "error")
        return redirect(url_for("employee.payroll_history"))

    success, message, detail, period = payroll_controller.get_payroll_detail_by_id(
        payroll_detail_id, employee_id
    )

    if not success or detail is None:
        flash(message, "error")
        return redirect(url_for("employee.payroll_history"))

    # Get employee info for salary type
    success, message, employee = employee_controller.get_employee(employee_id)
    salary_type = employee.salary_type if success and employee else None

    return render_template(
        "employee/paycheck_detail.html",
        payroll=detail,
        period=period,
        employee=employee,
        salary_type=salary_type,
    )


@bp.route("/paycheck/<int:payroll_detail_id>/pdf")
@login_required
def download_paycheck_pdf(payroll_detail_id):
    """Download employee's own paycheck as PDF."""
    employee_id = session.get("employee_id")

    if not employee_id:
        flash("Employee ID not found.", "error")
        return redirect(url_for("employee.payroll_history"))

    detail = PayrollDetail.get_by_id(payroll_detail_id)

    if detail is None or detail.employee_id != employee_id:
        flash("Payroll detail not found or access denied.", "error")
        return redirect(url_for("employee.payroll_history"))

    period = PayrollPeriod.get_by_id(detail.payroll_id)
    success, message, employee = employee_controller.get_employee(employee_id)

    # Generate PDF
    pdf_buffer = generate_paycheck_pdf(detail, period.period_start_date, period.period_end_date)

    # Create filename
    employee_name = f"{employee.first_name}_{employee.last_name}" if employee else detail.employee_id
    filename = f"paycheck_{detail.employee_id}_{employee_name}_{period.period_start_date}.pdf"

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf",
    )
