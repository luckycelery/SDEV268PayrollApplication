"""
Payroll Routes - Payroll management functionality

Handles:
- Payroll period listing
- Payroll calculation
- Payroll reports
"""

from flask import Blueprint, flash, redirect, render_template, session, url_for

from src.controllers.payroll_controller import PayrollController
from src.models.employee import Employee
from src.models.payroll import PayrollDetail, PayrollPeriod

bp = Blueprint("payroll", __name__)

# Initialize controller
payroll_controller = PayrollController()


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
@admin_required
def payroll_list():
    """List all payroll periods."""
    success, message, periods = payroll_controller.get_all_payroll_periods()

    return render_template("payroll/payroll_list.html", periods=periods)


@bp.route("/current")
@admin_required
def current_period():
    """View current pay period details."""
    start_date, end_date = payroll_controller.get_current_period()

    success, message, period = payroll_controller.get_or_create_payroll_period(
        start_date, end_date
    )

    # Get payroll details if period exists
    details = []
    if period and period.payroll_id:
        success, message, details = payroll_controller.get_payroll_details_for_period(
            period.payroll_id
        )

    return render_template(
        "payroll/payroll_detail.html",
        period=period,
        details=details,
        start_date=start_date,
        end_date=end_date,
    )


@bp.route("/calculate", methods=["POST"])
@admin_required
def calculate_payroll():
    """Calculate payroll for current period."""
    start_date, end_date = payroll_controller.get_current_period()

    success, message, results = payroll_controller.calculate_all_payroll(
        start_date, end_date
    )

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect(url_for("payroll.current_period"))


@bp.route("/approve/<int:payroll_id>", methods=["POST"])
@admin_required
def approve_payroll(payroll_id):
    """Approve and lock a payroll period."""
    approved_by = session.get("username", "Admin")

    success, message = payroll_controller.approve_payroll(payroll_id, approved_by)

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect(url_for("payroll.payroll_list"))


@bp.route("/report/<int:payroll_id>")
@admin_required
def payroll_report(payroll_id):
    """Generate payroll report for a period."""
    success, message, period = payroll_controller.get_payroll_period(payroll_id)

    if not success:
        flash(message, "error")
        return redirect(url_for("payroll.payroll_list"))

    # Get summary
    success, message, summary = payroll_controller.get_payroll_summary(
        period.period_start_date, period.period_end_date
    )

    # Get all details
    success, message, details = payroll_controller.get_payroll_details_for_period(payroll_id)

    return render_template(
        "payroll/payroll_report.html",
        period=period,
        summary=summary,
        details=details,
    )


@bp.route("/detail/<int:payroll_detail_id>")
@admin_required
def view_paycheck_detail(payroll_detail_id):
    """Admin view of an individual employee's paycheck detail."""

    detail = PayrollDetail.get_by_id(payroll_detail_id)

    if detail is None:
        flash("Payroll detail not found.", "error")
        return redirect(url_for("payroll.payroll_list"))

    period = PayrollPeriod.get_by_id(detail.payroll_id)
    employee = Employee.get_by_id(detail.employee_id)
    salary_type = employee.salary_type if employee else None

    return render_template(
        "employee/paycheck_detail.html",
        payroll=detail,
        period=period,
        is_admin_view=True,
        salary_type=salary_type,
    )
