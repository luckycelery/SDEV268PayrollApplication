"""
Admin Time Entry Management Route
Allows admins to view and edit time entries for any employee and period.
"""

from datetime import datetime, timedelta

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from src.controllers.employee_controller import EmployeeController
from src.controllers.payroll_controller import PayrollController
from src.models.payroll import PayrollPeriod
from src.models.time_entry import TimeEntry

from .admin import admin_required

bp = Blueprint("admin_time_entry", __name__)

employee_controller = EmployeeController()
payroll_controller = PayrollController()

@bp.route("/time-entries", methods=["GET"])
@admin_required
def time_entry_overview():
    """
    Admin overview: All unlocked periods with all employees and total hours.
    """
    # Get all unlocked pay periods
    unlocked_periods = PayrollPeriod.get_all(include_locked=False)

    # Get all active employees
    success, msg, employees = employee_controller.get_all_employees()

    # Build data structure: period -> list of (employee, total_hours, pto_used)
    period_data = []
    for period in unlocked_periods:
        employee_hours = []
        for employee in employees:
            # Get time entries for this employee in this period
            entries = TimeEntry.get_by_employee(
                employee.employee_id,
                period.period_start_date,
                period.period_end_date
            )
            total_hours = sum(entry.hours_worked + entry.pto_hours for entry in entries)
            pto_used = sum(entry.pto_hours for entry in entries)
            employee_hours.append({
                'employee': employee,
                'total_hours': total_hours,
                'pto_used': pto_used
            })

        period_data.append({
            'period': period,
            'employee_hours': employee_hours
        })

    return render_template(
        "admin/time_entry_admin.html",
        period_data=period_data,
    )


@bp.route("/time-entries/<employee_id>/<start_date>/<end_date>", methods=["GET", "POST"])
@admin_required
def time_entry_detail(employee_id, start_date, end_date):
    """
    Admin detail view: Daily breakdown for specific employee and period.
    """
    # Get employee
    success, msg, employee = employee_controller.get_employee(employee_id)
    if not success:
        flash(msg, "error")
        return redirect(url_for("admin_time_entry.time_entry_overview"))

    # Get period info
    period = PayrollPeriod.get_by_dates(start_date, end_date)

    if request.method == "POST":
        # Handle time entry submission/edit
        entry_date = request.form.get("entry_date", "")
        hours_worked = float(request.form.get("hours_worked") or 0)
        pto_hours = float(request.form.get("pto_hours") or 0)
        notes = request.form.get("notes", "").strip() or None

        # Call controller with is_admin=True
        success, message, entry = payroll_controller.submit_time_entry(
            employee_id=employee_id,
            entry_date=entry_date,
            hours_worked=hours_worked,
            pto_hours=pto_hours,
            notes=notes,
            is_admin=True,
        )
        if success:
            flash(message, "success")
        else:
            flash(message, "error")
        return redirect(url_for("admin_time_entry.time_entry_detail",
                               employee_id=employee_id,
                               start_date=start_date,
                               end_date=end_date))

    # Get existing time entries for this period
    existing_entries = TimeEntry.get_by_employee(employee_id, start_date, end_date)

    # Create a map of date -> entry for quick lookup
    entries_by_date = {entry.entry_date: entry for entry in existing_entries}

    # Generate all 7 days of the week (period should be Monday to Sunday)
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
    all_entries = []

    for day_offset in range(7):
        current_date = start_date_obj + timedelta(days=day_offset)
        date_str = current_date.strftime("%Y-%m-%d")

        # Use existing entry if available, otherwise create empty entry
        if date_str in entries_by_date:
            all_entries.append(entries_by_date[date_str])
        else:
            # Create a new empty entry for this date
            day_of_week = TimeEntry.get_day_of_week(date_str)
            is_saturday = 1 if day_of_week == "Saturday" else 0
            empty_entry = TimeEntry(
                employee_id=employee_id,
                entry_date=date_str,
                day_of_week=day_of_week,
                hours_worked=0.0,
                pto_hours=0.0,
                is_saturday=is_saturday,
                notes=None
            )
            all_entries.append(empty_entry)

    # Get pay preview
    pay_success, msg, pay_preview = payroll_controller.calculate_weekly_pay(
        employee_id, start_date, end_date
    )

    return render_template(
        "admin/time_entry_detail.html",
        employee=employee,
        period=period,
        entries=all_entries,
        start_date=start_date,
        end_date=end_date,
        pay_preview=pay_preview,
    )
