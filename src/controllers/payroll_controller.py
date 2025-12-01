"""
Payroll Controller - Business logic for payroll processing
Coordinates between UI, TimeEntry model, and Payroll models
"""

from datetime import datetime, timedelta

from src.models.employee import Employee
from src.models.payroll import PayrollCalculator, PayrollDetail, PayrollPeriod
from src.models.time_entry import TimeEntry
from src.utils.constants import (
    EMPLOYEE_STATUS_ACTIVE,
    SALARIED_AUTO_HOURS_PER_DAY,
    SALARIED_WORK_DAYS,
    SALARY_TYPE_HOURLY,
    SALARY_TYPE_SALARY,
    STANDARD_WORK_HOURS_PER_WEEK,
)


class PayrollController:
    """
    Controller for payroll processing operations

    Handles:
    - Time entry management (CRUD)
    - Payroll calculation for hourly and salaried employees
    - Payroll period management
    - Payroll history retrieval
    """

    def __init__(self):
        """Initialize payroll controller."""
        self.calculator = PayrollCalculator()

    # =========================================================================
    # PAY PERIOD OPERATIONS
    # =========================================================================

    def get_current_period(self) -> tuple[str, str]:
        """
        Get the current pay period dates (Monday to Sunday).

        Returns:
            Tuple of (start_date, end_date) in YYYY-MM-DD format
        """
        return PayrollPeriod.get_current_period()

    def get_period_for_date(self, date_str: str) -> tuple[str, str]:
        """
        Get the pay period containing a specific date.

        Args:
            date_str: Date in YYYY-MM-DD format

        Returns:
            Tuple of (start_date, end_date) in YYYY-MM-DD format
        """
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        days_since_monday = date_obj.weekday()
        monday = date_obj - timedelta(days=days_since_monday)
        sunday = monday + timedelta(days=6)

        return monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")

    def get_or_create_payroll_period(
        self, start_date: str, end_date: str
    ) -> tuple[bool, str, PayrollPeriod | None]:
        """
        Get existing or create new payroll period.

        Args:
            start_date: Period start date (Monday)
            end_date: Period end date (Sunday)

        Returns:
            Tuple of (success, message, payroll_period)
        """
        try:
            period = PayrollPeriod.get_or_create(start_date, end_date)
            return True, f"Payroll period {start_date} to {end_date}", period
        except Exception as e:
            return False, f"Error with payroll period: {e!s}", None

    def get_payroll_period(self, payroll_id: int) -> tuple[bool, str, PayrollPeriod | None]:
        """
        Get payroll period by ID.

        Args:
            payroll_id: Payroll period ID

        Returns:
            Tuple of (success, message, payroll_period)
        """
        try:
            period = PayrollPeriod.get_by_id(payroll_id)
            if period:
                return True, "Payroll period found", period
            return False, f"Payroll period {payroll_id} not found", None
        except Exception as e:
            return False, f"Error retrieving payroll period: {e!s}", None

    def get_all_payroll_periods(
        self, include_locked: bool = True
    ) -> tuple[bool, str, list[PayrollPeriod]]:
        """
        Get all payroll periods.

        Args:
            include_locked: Include locked/processed periods

        Returns:
            Tuple of (success, message, list_of_periods)
        """
        try:
            periods = PayrollPeriod.get_all(include_locked=include_locked)
            return True, f"Retrieved {len(periods)} payroll periods", periods
        except Exception as e:
            return False, f"Error retrieving payroll periods: {e!s}", []

    # =========================================================================
    # TIME ENTRY OPERATIONS
    # =========================================================================

    def submit_time_entry(
        self,
        employee_id: str,
        entry_date: str,
        hours_worked: float,
        pto_hours: float = 0.0,
        notes: str | None = None,
    ) -> tuple[bool, str, TimeEntry | None]:
        """
        Submit or update a time entry for an employee.

        Args:
            employee_id: Employee ID
            entry_date: Date of entry (YYYY-MM-DD)
            hours_worked: Hours worked
            pto_hours: PTO hours used
            notes: Optional notes

        Returns:
            Tuple of (success, message, time_entry)
        """
        try:
            # Check if employee exists and is active
            employee = Employee.get_by_id(employee_id)
            if not employee:
                return False, f"Employee {employee_id} not found", None
            if employee.status != EMPLOYEE_STATUS_ACTIVE:
                return False, f"Employee {employee_id} is not active", None

            # Check if entry already exists for this date
            existing = TimeEntry.get_by_employee_and_date(employee_id, entry_date)

            if existing:
                # Check if payroll is locked
                if existing.payroll_id:
                    period = PayrollPeriod.get_by_id(existing.payroll_id)
                    if period and period.is_locked:
                        return False, "Cannot edit time entry - payroll period is locked", None

                # Update existing entry
                existing.hours_worked = hours_worked
                existing.pto_hours = pto_hours
                existing.notes = notes

                errors = existing.validate()
                if errors:
                    return False, f"Validation failed: {', '.join(errors)}", None

                if existing.save():
                    return True, f"Time entry updated for {entry_date}", existing
                return False, "Failed to update time entry", None
            else:
                # Create new entry
                entry = TimeEntry.create_entry(
                    employee_id=employee_id,
                    entry_date=entry_date,
                    hours_worked=hours_worked,
                    pto_hours=pto_hours,
                    notes=notes,
                )

                errors = entry.validate()
                if errors:
                    return False, f"Validation failed: {', '.join(errors)}", None

                if entry.save():
                    return True, f"Time entry created for {entry_date}", entry
                return False, "Failed to create time entry", None

        except Exception as e:
            return False, f"Error submitting time entry: {e!s}", None

    def get_time_entry(
        self, employee_id: str, entry_date: str
    ) -> tuple[bool, str, TimeEntry | None]:
        """
        Get a specific time entry.

        Args:
            employee_id: Employee ID
            entry_date: Date of entry (YYYY-MM-DD)

        Returns:
            Tuple of (success, message, time_entry)
        """
        try:
            entry = TimeEntry.get_by_employee_and_date(employee_id, entry_date)
            if entry:
                return True, "Time entry found", entry
            return False, f"No time entry found for {employee_id} on {entry_date}", None
        except Exception as e:
            return False, f"Error retrieving time entry: {e!s}", None

    def get_time_entries(
        self,
        employee_id: str,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> tuple[bool, str, list[TimeEntry]]:
        """
        Get time entries for an employee within date range.

        Args:
            employee_id: Employee ID
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            Tuple of (success, message, list_of_entries)
        """
        try:
            entries = TimeEntry.get_by_employee(employee_id, start_date, end_date)
            return True, f"Found {len(entries)} time entries", entries
        except Exception as e:
            return False, f"Error retrieving time entries: {e!s}", []

    def get_weekly_time_entries(
        self, employee_id: str, week_start: str
    ) -> tuple[bool, str, list[TimeEntry]]:
        """
        Get time entries for a specific week (Monday-Sunday).

        Args:
            employee_id: Employee ID
            week_start: Monday date of the week (YYYY-MM-DD)

        Returns:
            Tuple of (success, message, list_of_entries)
        """
        try:
            start_date, end_date = self.get_period_for_date(week_start)
            entries = TimeEntry.get_by_employee(employee_id, start_date, end_date)
            return True, f"Found {len(entries)} entries for week of {start_date}", entries
        except Exception as e:
            return False, f"Error retrieving weekly time entries: {e!s}", []

    def delete_time_entry(
        self, employee_id: str, entry_date: str
    ) -> tuple[bool, str]:
        """
        Delete a time entry.

        Args:
            employee_id: Employee ID
            entry_date: Date of entry (YYYY-MM-DD)

        Returns:
            Tuple of (success, message)
        """
        try:
            entry = TimeEntry.get_by_employee_and_date(employee_id, entry_date)
            if not entry:
                return False, f"No time entry found for {employee_id} on {entry_date}"

            # Check if payroll is locked
            if entry.payroll_id:
                period = PayrollPeriod.get_by_id(entry.payroll_id)
                if period and period.is_locked:
                    return False, "Cannot delete time entry - payroll period is locked"

            if entry.delete():
                return True, f"Time entry deleted for {entry_date}"
            return False, "Failed to delete time entry"
        except Exception as e:
            return False, f"Error deleting time entry: {e!s}"

    # =========================================================================
    # PAYROLL CALCULATION
    # =========================================================================

    def calculate_weekly_pay(
        self,
        employee_id: str,
        start_date: str,
        end_date: str,
    ) -> tuple[bool, str, PayrollDetail | None]:
        """
        Calculate weekly payroll for an employee.

        Args:
            employee_id: Employee ID
            start_date: Period start date (Monday)
            end_date: Period end date (Sunday)

        Returns:
            Tuple of (success, message, payroll_detail)
        """
        try:
            # Get employee
            employee = Employee.get_by_id(employee_id)
            if not employee:
                return False, f"Employee {employee_id} not found", None

            # Get or create payroll period
            period = PayrollPeriod.get_or_create(start_date, end_date)

            # Check if already calculated
            if period.payroll_id is None:
                return False, "Failed to get payroll period ID", None

            existing = PayrollDetail.get_by_payroll_and_employee(
                period.payroll_id, employee_id
            )
            if existing and period.is_locked:
                return True, "Payroll already calculated and locked", existing

            # Get time entries for the period
            entries = TimeEntry.get_by_employee(employee_id, start_date, end_date)

            # Calculate pay based on salary type
            if employee.salary_type == SALARY_TYPE_SALARY:
                if employee.base_salary is None:
                    return False, "Salaried employee has no base salary set", None
                pay_data = self.calculator.calculate_salary_pay(employee.base_salary)
            elif employee.salary_type == SALARY_TYPE_HOURLY:
                if employee.hourly_rate is None:
                    return False, "Hourly employee has no hourly rate set", None
                pay_data = self.calculator.calculate_hourly_pay(
                    entries, employee.hourly_rate
                )
            else:
                return False, f"Unknown salary type: {employee.salary_type}", None

            # Calculate dependent stipend (additional income)
            dependent_stipend = self.calculator.calculate_dependent_stipend(
                employee.num_dependents or 0
            )

            # Calculate medical deduction
            medical_deduction = self.calculator.calculate_medical_deduction(
                employee.medical_type or "Single"
            )

            # Gross pay includes base pay + dependent stipend
            gross_pay = pay_data["gross_pay"] + dependent_stipend

            # Taxable income = gross pay - medical deduction
            taxable_income = gross_pay - medical_deduction

            # Calculate taxes based on taxable income
            tax_data = self.calculator.calculate_taxes(taxable_income)

            # Calculate net pay
            net_data = self.calculator.calculate_net_pay(
                gross_pay,
                medical_deduction,
                tax_data["total_employee_taxes"],
            )

            # Create or update payroll detail
            detail = existing or PayrollDetail(
                payroll_id=period.payroll_id,
                employee_id=employee_id,
            )

            # Update all fields
            detail.regular_hours = pay_data["regular_hours"]
            detail.overtime_hours = pay_data["overtime_hours"]
            detail.saturday_hours = pay_data["saturday_hours"]
            detail.pto_hours = pay_data["pto_hours"]
            detail.total_hours = pay_data["total_hours"]

            detail.base_pay = pay_data["base_pay"]
            detail.overtime_pay = pay_data["overtime_pay"]
            detail.saturday_pay = pay_data["saturday_pay"]
            detail.gross_pay = gross_pay  # Includes dependent stipend

            detail.medical_deduction = medical_deduction
            detail.dependent_stipend = dependent_stipend
            detail.taxable_income = taxable_income

            detail.state_tax = tax_data["state_tax"]
            detail.federal_tax_employee = tax_data["federal_tax_employee"]
            detail.social_security_employee = tax_data["social_security_employee"]
            detail.medicare_employee = tax_data["medicare_employee"]
            detail.total_employee_taxes = tax_data["total_employee_taxes"]

            detail.net_pay = net_data["net_pay"]

            detail.federal_tax_employer = tax_data["federal_tax_employer"]
            detail.social_security_employer = tax_data["social_security_employer"]
            detail.medicare_employer = tax_data["medicare_employer"]
            detail.total_employer_taxes = tax_data["total_employer_taxes"]

            # Save
            if detail.save():
                # Assign time entries to this payroll period
                TimeEntry.assign_to_payroll(
                    employee_id, start_date, end_date, period.payroll_id
                )
                return True, f"Payroll calculated: Net pay ${detail.net_pay:.2f}", detail

            return False, "Failed to save payroll detail", None

        except Exception as e:
            return False, f"Error calculating payroll: {e!s}", None

    def calculate_all_payroll(
        self,
        start_date: str,
        end_date: str,
        active_only: bool = True,
    ) -> tuple[bool, str, list[PayrollDetail]]:
        """
        Calculate payroll for all employees for a pay period.

        Args:
            start_date: Period start date (Monday)
            end_date: Period end date (Sunday)
            active_only: Only include active employees

        Returns:
            Tuple of (success, message, list_of_payroll_details)
        """
        try:
            employees = Employee.get_all(include_terminated=not active_only)
            results = []
            errors = []

            for employee in employees:
                success, msg, detail = self.calculate_weekly_pay(
                    employee.employee_id, start_date, end_date
                )
                if success and detail:
                    results.append(detail)
                else:
                    errors.append(f"{employee.employee_id}: {msg}")

            if errors:
                return (
                    True,
                    f"Calculated {len(results)} payrolls with {len(errors)} errors",
                    results,
                )
            return True, f"Successfully calculated payroll for {len(results)} employees", results

        except Exception as e:
            return False, f"Error calculating payroll: {e!s}", []

    def approve_payroll(
        self,
        payroll_id: int,
        approved_by: str,
    ) -> tuple[bool, str]:
        """
        Approve and lock a payroll period.

        Args:
            payroll_id: Payroll period ID
            approved_by: Username of approver

        Returns:
            Tuple of (success, message)
        """
        try:
            period = PayrollPeriod.get_by_id(payroll_id)
            if not period:
                return False, f"Payroll period {payroll_id} not found"

            if period.is_locked:
                return False, "Payroll period is already locked"

            if period.lock(approved_by):
                return True, f"Payroll period approved by {approved_by}"
            return False, "Failed to approve payroll period"

        except Exception as e:
            return False, f"Error approving payroll: {e!s}"

    # =========================================================================
    # PAYROLL HISTORY
    # =========================================================================

    def get_payroll_history(
        self,
        employee_id: str,
        limit: int | None = None,
    ) -> tuple[bool, str, list[PayrollDetail]]:
        """
        Get payroll history for an employee.

        Args:
            employee_id: Employee ID
            limit: Maximum number of records to return

        Returns:
            Tuple of (success, message, list_of_payroll_details)
        """
        try:
            history = PayrollDetail.get_by_employee(employee_id, limit)
            return True, f"Retrieved {len(history)} payroll records", history
        except Exception as e:
            return False, f"Error retrieving payroll history: {e!s}", []

    def get_payroll_details_for_period(
        self, payroll_id: int
    ) -> tuple[bool, str, list[PayrollDetail]]:
        """
        Get all payroll details for a pay period.

        Args:
            payroll_id: Payroll period ID

        Returns:
            Tuple of (success, message, list_of_payroll_details)
        """
        try:
            details = PayrollDetail.get_by_payroll(payroll_id)
            return True, f"Retrieved {len(details)} payroll details", details
        except Exception as e:
            return False, f"Error retrieving payroll details: {e!s}", []

    def get_employee_payroll(
        self,
        employee_id: str,
        payroll_id: int,
    ) -> tuple[bool, str, PayrollDetail | None]:
        """
        Get specific payroll detail for employee and period.

        Args:
            employee_id: Employee ID
            payroll_id: Payroll period ID

        Returns:
            Tuple of (success, message, payroll_detail)
        """
        try:
            detail = PayrollDetail.get_by_payroll_and_employee(payroll_id, employee_id)
            if detail:
                return True, "Payroll detail found", detail
            return False, "No payroll detail found for this period", None
        except Exception as e:
            return False, f"Error retrieving payroll detail: {e!s}", None

    # =========================================================================
    # SUMMARY REPORTS
    # =========================================================================

    def get_payroll_summary(
        self,
        start_date: str,
        end_date: str,
    ) -> tuple[bool, str, dict]:
        """
        Get payroll summary for a pay period.

        Args:
            start_date: Period start date
            end_date: Period end date

        Returns:
            Tuple of (success, message, summary_dict)
        """
        try:
            period = PayrollPeriod.get_by_dates(start_date, end_date)
            if not period:
                return False, "Payroll period not found", {}

            if period.payroll_id is None:
                return False, "Payroll period has no ID", {}

            details = PayrollDetail.get_by_payroll(period.payroll_id)

            summary = {
                "period": {
                    "start_date": start_date,
                    "end_date": end_date,
                    "payroll_id": period.payroll_id,
                    "is_locked": period.is_locked,
                    "processed_date": period.processed_date,
                    "processed_by": period.processed_by,
                },
                "employee_count": len(details),
                "totals": {
                    "total_hours": sum(d.total_hours for d in details),
                    "total_regular_hours": sum(d.regular_hours for d in details),
                    "total_overtime_hours": sum(d.overtime_hours for d in details),
                    "total_saturday_hours": sum(d.saturday_hours for d in details),
                    "total_pto_hours": sum(d.pto_hours for d in details),
                    "total_gross_pay": round(sum(d.gross_pay for d in details), 2),
                    "total_net_pay": round(sum(d.net_pay for d in details), 2),
                    "total_employee_taxes": round(sum(d.total_employee_taxes for d in details), 2),
                    "total_employer_taxes": round(sum(d.total_employer_taxes for d in details), 2),
                    "total_medical_deductions": round(sum(d.medical_deduction for d in details), 2),
                    "total_dependent_stipends": round(sum(d.dependent_stipend for d in details), 2),
                },
            }

            return True, "Payroll summary generated", summary

        except Exception as e:
            return False, f"Error generating payroll summary: {e!s}", {}

    def get_employee_weekly_summary(
        self,
        employee_id: str,
        start_date: str,
        end_date: str,
    ) -> tuple[bool, str, dict]:
        """
        Get weekly time and pay summary for an employee.

        Args:
            employee_id: Employee ID
            start_date: Period start date
            end_date: Period end date

        Returns:
            Tuple of (success, message, summary_dict)
        """
        try:
            employee = Employee.get_by_id(employee_id)
            if not employee:
                return False, f"Employee {employee_id} not found", {}

            entries = TimeEntry.get_by_employee(employee_id, start_date, end_date)

            # Calculate totals from entries
            total_hours = sum(e.hours_worked for e in entries)
            total_pto = sum(e.pto_hours for e in entries)
            saturday_hours = sum(e.hours_worked for e in entries if e.is_saturday)

            # Calculate overtime (hours over 40)
            regular_hours = min(total_hours - saturday_hours, STANDARD_WORK_HOURS_PER_WEEK)
            overtime_hours = max(0, (total_hours - saturday_hours) - STANDARD_WORK_HOURS_PER_WEEK)

            summary = {
                "employee": {
                    "employee_id": employee_id,
                    "name": employee.get_full_name(),
                    "salary_type": employee.salary_type,
                    "hourly_rate": employee.hourly_rate,
                    "base_salary": employee.base_salary,
                },
                "period": {
                    "start_date": start_date,
                    "end_date": end_date,
                },
                "entries": [e.to_dict() for e in entries],
                "hours": {
                    "regular": regular_hours,
                    "overtime": overtime_hours,
                    "saturday": saturday_hours,
                    "pto": total_pto,
                    "total": total_hours + total_pto,
                },
            }

            return True, "Weekly summary generated", summary

        except Exception as e:
            return False, f"Error generating weekly summary: {e!s}", {}

    # =========================================================================
    # AUTO-FILL SALARIED HOURS
    # =========================================================================

    def auto_fill_salaried_hours(
        self,
        employee_id: str,
        start_date: str,
        end_date: str,
    ) -> tuple[bool, str, list[TimeEntry]]:
        """
        Auto-fill time entries for salaried employees (8 hours Mon-Fri).

        Args:
            employee_id: Employee ID
            start_date: Period start date (Monday)
            end_date: Period end date (Sunday)

        Returns:
            Tuple of (success, message, list_of_created_entries)
        """
        try:
            employee = Employee.get_by_id(employee_id)
            if not employee:
                return False, f"Employee {employee_id} not found", []

            if employee.salary_type != SALARY_TYPE_SALARY:
                return False, "Auto-fill is only for salaried employees", []

            created = []
            current_date = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")

            while current_date <= end:
                day_name = TimeEntry.get_day_of_week(current_date.strftime("%Y-%m-%d"))

                if day_name in SALARIED_WORK_DAYS:
                    date_str = current_date.strftime("%Y-%m-%d")

                    # Check if entry already exists
                    existing = TimeEntry.get_by_employee_and_date(employee_id, date_str)
                    if not existing:
                        entry = TimeEntry.create_entry(
                            employee_id=employee_id,
                            entry_date=date_str,
                            hours_worked=SALARIED_AUTO_HOURS_PER_DAY,
                            pto_hours=0.0,
                            notes="Auto-filled for salaried employee",
                        )
                        if entry.save():
                            created.append(entry)

                current_date += timedelta(days=1)

            return True, f"Created {len(created)} time entries", created

        except Exception as e:
            return False, f"Error auto-filling hours: {e!s}", []
