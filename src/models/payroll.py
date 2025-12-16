"""
Payroll Model - Represents payroll calculation results for employees
Matches the payroll_periods and payroll_details tables in database/schema.sql
"""

import sqlite3
from datetime import datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal
from typing import Optional

from src.utils.constants import (
    DEPENDENT_STIPEND_PER_DEPENDENT,
    FEDERAL_TAX_BRACKETS_ANNUAL,
    FEDERAL_TAX_RATE_EMPLOYEE,
    FEDERAL_TAX_RATE_EMPLOYER,
    MEDICAL_DEDUCTION_FAMILY,
    MEDICAL_DEDUCTION_SINGLE,
    MEDICAL_TYPE_FAMILY,
    MEDICARE_RATE_EMPLOYEE,
    MEDICARE_RATE_EMPLOYER,
    OVERTIME_MULTIPLIER,
    SATURDAY_MULTIPLIER,
    SOCIAL_SECURITY_RATE_EMPLOYEE,
    SOCIAL_SECURITY_RATE_EMPLOYER,
    STANDARD_WORK_HOURS_PER_WEEK,
    STATE_TAX_RATE_IN,
    WEEKS_PER_YEAR,
)

from .base_model import BaseModel


def _calculate_federal_tax_progressive(annual_taxable_income: float) -> float:
    """
    Calculate federal income tax using progressive brackets.
    
    NOTE: This function is preserved for future implementation of accurate
    progressive tax calculation. Currently the project uses a flat 7.65% rate.

    Args:
        annual_taxable_income: Projected annual taxable income

    Returns:
        Annual federal tax amount
    """
    tax = 0.0
    previous_limit = 0.0

    for bracket_limit, rate in FEDERAL_TAX_BRACKETS_ANNUAL:
        if annual_taxable_income <= previous_limit:
            break

        # Calculate taxable amount in this bracket
        taxable_in_bracket = min(annual_taxable_income, bracket_limit) - previous_limit
        tax += taxable_in_bracket * rate
        previous_limit = bracket_limit

    return tax


class PayrollPeriod(BaseModel):
    """
    PayrollPeriod model - represents a weekly pay period (Monday-Sunday)

    Matches the payroll_periods table in database.
    """

    def __init__(
        self,
        period_start_date: str,
        period_end_date: str,
        payroll_id: int | None = None,
        processed_date: str | None = None,
        is_locked: int = 0,
        processed_by: str | None = None,
        created_date: str | None = None,
    ):
        """
        Initialize PayrollPeriod object.

        Args:
            period_start_date: Monday of the pay week (YYYY-MM-DD)
            period_end_date: Sunday of the pay week (YYYY-MM-DD)
            payroll_id: Auto-generated primary key
            processed_date: When payroll was calculated (NULL until processed)
            is_locked: 1 if locked (no edits allowed), 0 otherwise
            processed_by: Admin username who processed
            created_date: Timestamp of record creation
        """
        self.payroll_id = payroll_id
        self.period_start_date = period_start_date
        self.period_end_date = period_end_date
        self.processed_date = processed_date
        self.is_locked = is_locked
        self.processed_by = processed_by
        self.created_date = created_date

    @property
    def is_locked_bool(self) -> bool:
        """Return is_locked as boolean."""
        return self.is_locked == 1

    @property
    def is_processed(self) -> bool:
        """Check if payroll has been processed."""
        return self.processed_date is not None

    # =========================================================================
    # DATABASE OPERATIONS
    # =========================================================================

    def save(self) -> bool:
        """Save payroll period to database."""
        if self.payroll_id is None:
            return self._insert()
        else:
            return self._update()

    def _insert(self) -> bool:
        """Insert new payroll period."""
        query = """
            INSERT INTO payroll_periods (
                period_start_date, period_end_date, processed_date,
                is_locked, processed_by
            ) VALUES (?, ?, ?, ?, ?)
        """
        params = (
            self.period_start_date,
            self.period_end_date,
            self.processed_date,
            self.is_locked,
            self.processed_by,
        )

        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            self.payroll_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def _update(self) -> bool:
        """Update existing payroll period."""
        query = """
            UPDATE payroll_periods SET
                period_start_date = ?,
                period_end_date = ?,
                processed_date = ?,
                is_locked = ?,
                processed_by = ?
            WHERE payroll_id = ?
        """
        params = (
            self.period_start_date,
            self.period_end_date,
            self.processed_date,
            self.is_locked,
            self.processed_by,
            self.payroll_id,
        )
        affected = self.execute_write(query, params)
        return affected > 0

    def lock(self, processed_by: str) -> bool:
        """Lock the payroll period (no more edits allowed)."""
        self.is_locked = 1
        self.processed_date = datetime.now().isoformat()
        self.processed_by = processed_by
        return self.save()

    @classmethod
    def get_by_id(cls, payroll_id: int) -> Optional["PayrollPeriod"]:
        """Get payroll period by ID."""
        query = "SELECT * FROM payroll_periods WHERE payroll_id = ?"
        row = cls.execute_single(query, (payroll_id,))

        if row is None:
            return None

        return cls._row_to_payroll_period(row)

    @classmethod
    def get_by_dates(
        cls, start_date: str, end_date: str
    ) -> Optional["PayrollPeriod"]:
        """Get payroll period by start and end dates."""
        query = """
            SELECT * FROM payroll_periods
            WHERE period_start_date = ? AND period_end_date = ?
        """
        row = cls.execute_single(query, (start_date, end_date))

        if row is None:
            return None

        return cls._row_to_payroll_period(row)

    @classmethod
    def get_or_create(cls, start_date: str, end_date: str) -> "PayrollPeriod":
        """Get existing payroll period or create new one."""
        existing = cls.get_by_dates(start_date, end_date)
        if existing:
            return existing

        new_period = PayrollPeriod(
            period_start_date=start_date,
            period_end_date=end_date,
        )
        new_period.save()
        return new_period

    @classmethod
    def get_all(cls, include_locked: bool = True) -> list["PayrollPeriod"]:
        """Get all payroll periods."""
        if include_locked:
            query = "SELECT * FROM payroll_periods ORDER BY period_start_date DESC"
            params = ()
        else:
            query = """
                SELECT * FROM payroll_periods
                WHERE is_locked = 0
                ORDER BY period_start_date DESC
            """
            params = ()

        rows = cls.execute_query(query, params)
        return [cls._row_to_payroll_period(row) for row in rows]

    @classmethod
    def _row_to_payroll_period(cls, row: sqlite3.Row) -> "PayrollPeriod":
        """Convert database row to PayrollPeriod object."""
        return PayrollPeriod(
            payroll_id=row["payroll_id"],
            period_start_date=row["period_start_date"],
            period_end_date=row["period_end_date"],
            processed_date=row["processed_date"],
            is_locked=row["is_locked"],
            processed_by=row["processed_by"],
            created_date=row["created_date"],
        )

    @classmethod
    def get_current_period(cls) -> tuple[str, str]:
        """
        Get the current pay period dates (Monday to Sunday containing today).

        Returns:
            Tuple of (start_date, end_date) in YYYY-MM-DD format
        """
        today = datetime.now().date()
        # Find Monday of current week
        days_since_monday = today.weekday()  # Monday = 0
        monday = today - timedelta(days=days_since_monday)
        sunday = monday + timedelta(days=6)

        return monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "payroll_id": self.payroll_id,
            "period_start_date": self.period_start_date,
            "period_end_date": self.period_end_date,
            "processed_date": self.processed_date,
            "is_locked": self.is_locked,
            "processed_by": self.processed_by,
            "created_date": self.created_date,
        }


class PayrollDetail(BaseModel):
    """
    PayrollDetail model - represents calculated payroll for one employee in one period

    Matches the payroll_details table in database.
    Contains all hours, pay, deductions, taxes, and net pay calculations.
    """

    def __init__(
        self,
        payroll_id: int,
        employee_id: str,
        # Hours
        regular_hours: float = 0.0,
        overtime_hours: float = 0.0,
        saturday_hours: float = 0.0,
        pto_hours: float = 0.0,
        total_hours: float = 0.0,
        # Pay
        base_pay: float = 0.0,
        overtime_pay: float = 0.0,
        saturday_pay: float = 0.0,
        dependent_stipend: float = 0.0,
        gross_pay: float = 0.0,
        # Deductions
        medical_deduction: float = 0.0,
        total_employee_deductions: float = 0.0,
        # Taxable income
        taxable_income: float = 0.0,
        # Employee taxes
        state_tax: float = 0.0,
        federal_tax_employee: float = 0.0,
        social_security_employee: float = 0.0,
        medicare_employee: float = 0.0,
        total_employee_taxes: float = 0.0,
        # Net pay
        net_pay: float = 0.0,
        # Employer taxes
        federal_tax_employer: float = 0.0,
        social_security_employer: float = 0.0,
        medicare_employer: float = 0.0,
        total_employer_taxes: float = 0.0,
        # Metadata
        payroll_detail_id: int | None = None,
        calculated_date: str | None = None,
        # Period info (optional - populated from joins)
        period_start_date: str | None = None,
        period_end_date: str | None = None,
    ):
        """
        Initialize PayrollDetail with all calculation fields.
        """
        self.payroll_detail_id = payroll_detail_id
        self.payroll_id = payroll_id
        self.employee_id = employee_id
        # Period info (populated by get_by_employee)
        self.period_start_date = period_start_date
        self.period_end_date = period_end_date

        # Hours
        self.regular_hours = regular_hours
        self.overtime_hours = overtime_hours
        self.saturday_hours = saturday_hours
        self.pto_hours = pto_hours
        self.total_hours = total_hours

        # Pay
        self.base_pay = base_pay
        self.overtime_pay = overtime_pay
        self.saturday_pay = saturday_pay
        self.gross_pay = gross_pay
        self.dependent_stipend = dependent_stipend

        # Deductions
        self.medical_deduction = medical_deduction
        self.total_employee_deductions = total_employee_deductions

        # Taxable income
        self.taxable_income = taxable_income

        # Employee taxes
        self.state_tax = state_tax
        self.federal_tax_employee = federal_tax_employee
        self.social_security_employee = social_security_employee
        self.medicare_employee = medicare_employee
        self.total_employee_taxes = total_employee_taxes

        # Net pay
        self.net_pay = net_pay

        # Employer taxes
        self.federal_tax_employer = federal_tax_employer
        self.social_security_employer = social_security_employer
        self.medicare_employer = medicare_employer
        self.total_employer_taxes = total_employer_taxes

        # Metadata
        self.calculated_date = calculated_date

    # =========================================================================
    # DATABASE OPERATIONS
    # =========================================================================

    def save(self) -> bool:
        """Save payroll detail to database."""
        if self.payroll_detail_id is None:
            return self._insert()
        else:
            return self._update()

    def _insert(self) -> bool:
        """Insert new payroll detail."""
        query = """
            INSERT INTO payroll_details (
                payroll_id, employee_id,
                regular_hours, overtime_hours, saturday_hours, pto_hours, total_hours,
                base_pay, overtime_pay, saturday_pay, gross_pay,
                medical_deduction, dependent_stipend, taxable_income,
                state_tax, federal_tax_employee, social_security_employee,
                medicare_employee, total_employee_taxes,
                net_pay,
                federal_tax_employer, social_security_employer, medicare_employer,
                total_employer_taxes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            self.payroll_id,
            self.employee_id,
            self.regular_hours,
            self.overtime_hours,
            self.saturday_hours,
            self.pto_hours,
            self.total_hours,
            self.base_pay,
            self.overtime_pay,
            self.saturday_pay,
            self.gross_pay,
            self.medical_deduction,
            self.dependent_stipend,
            self.taxable_income,
            self.state_tax,
            self.federal_tax_employee,
            self.social_security_employee,
            self.medicare_employee,
            self.total_employee_taxes,
            self.net_pay,
            self.federal_tax_employer,
            self.social_security_employer,
            self.medicare_employer,
            self.total_employer_taxes,
        )

        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            self.payroll_detail_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def _update(self) -> bool:
        """Update existing payroll detail."""
        query = """
            UPDATE payroll_details SET
                payroll_id = ?, employee_id = ?,
                regular_hours = ?, overtime_hours = ?, saturday_hours = ?,
                pto_hours = ?, total_hours = ?,
                base_pay = ?, overtime_pay = ?, saturday_pay = ?, gross_pay = ?,
                medical_deduction = ?, dependent_stipend = ?, taxable_income = ?,
                state_tax = ?, federal_tax_employee = ?, social_security_employee = ?,
                medicare_employee = ?, total_employee_taxes = ?,
                net_pay = ?,
                federal_tax_employer = ?, social_security_employer = ?,
                medicare_employer = ?, total_employer_taxes = ?
            WHERE payroll_detail_id = ?
        """
        params = (
            self.payroll_id,
            self.employee_id,
            self.regular_hours,
            self.overtime_hours,
            self.saturday_hours,
            self.pto_hours,
            self.total_hours,
            self.base_pay,
            self.overtime_pay,
            self.saturday_pay,
            self.gross_pay,
            self.medical_deduction,
            self.dependent_stipend,
            self.taxable_income,
            self.state_tax,
            self.federal_tax_employee,
            self.social_security_employee,
            self.medicare_employee,
            self.total_employee_taxes,
            self.net_pay,
            self.federal_tax_employer,
            self.social_security_employer,
            self.medicare_employer,
            self.total_employer_taxes,
            self.payroll_detail_id,
        )
        affected = self.execute_write(query, params)
        return affected > 0

    @classmethod
    def get_by_id(cls, payroll_detail_id: int) -> Optional["PayrollDetail"]:
        """Get payroll detail by ID."""
        query = "SELECT * FROM payroll_details WHERE payroll_detail_id = ?"
        row = cls.execute_single(query, (payroll_detail_id,))

        if row is None:
            return None

        return cls._row_to_payroll_detail(row)

    @classmethod
    def get_by_payroll_and_employee(
        cls, payroll_id: int, employee_id: str
    ) -> Optional["PayrollDetail"]:
        """Get payroll detail for specific payroll period and employee."""
        query = """
            SELECT * FROM payroll_details
            WHERE payroll_id = ? AND employee_id = ?
        """
        row = cls.execute_single(query, (payroll_id, employee_id))

        if row is None:
            return None

        return cls._row_to_payroll_detail(row)

    @classmethod
    def get_by_payroll(cls, payroll_id: int) -> list["PayrollDetail"]:
        """Get all payroll details for a payroll period."""
        query = """
            SELECT pd.*, e.first_name, e.last_name
            FROM payroll_details pd
            LEFT JOIN employees e ON pd.employee_id = e.employee_id
            WHERE pd.payroll_id = ?
            ORDER BY pd.employee_id
        """
        rows = cls.execute_query(query, (payroll_id,))
        return [cls._row_to_payroll_detail(row) for row in rows]

    @classmethod
    def get_by_employee(
        cls, employee_id: str, limit: int | None = None
    ) -> list["PayrollDetail"]:
        """Get payroll history for an employee."""
        if limit:
            query = """
                SELECT pd.*, pp.period_start_date, pp.period_end_date
                FROM payroll_details pd
                JOIN payroll_periods pp ON pd.payroll_id = pp.payroll_id
                WHERE pd.employee_id = ?
                ORDER BY pp.period_start_date DESC
                LIMIT ?
            """
            params = (employee_id, limit)
        else:
            query = """
                SELECT pd.*, pp.period_start_date, pp.period_end_date
                FROM payroll_details pd
                JOIN payroll_periods pp ON pd.payroll_id = pp.payroll_id
                WHERE pd.employee_id = ?
                ORDER BY pp.period_start_date DESC
            """
            params = (employee_id,)

        rows = cls.execute_query(query, params)
        return [cls._row_to_payroll_detail(row) for row in rows]

    @classmethod
    def _row_to_payroll_detail(cls, row: sqlite3.Row) -> "PayrollDetail":
        """Convert database row to PayrollDetail object."""
        # Get optional fields (may not be present in all queries)
        row_keys = row.keys()
        period_start = row["period_start_date"] if "period_start_date" in row_keys else None
        period_end = row["period_end_date"] if "period_end_date" in row_keys else None
        first_name = row["first_name"] if "first_name" in row_keys else None
        last_name = row["last_name"] if "last_name" in row_keys else None

        detail = PayrollDetail(
            payroll_detail_id=row["payroll_detail_id"],
            payroll_id=row["payroll_id"],
            employee_id=row["employee_id"],
            regular_hours=row["regular_hours"],
            overtime_hours=row["overtime_hours"],
            saturday_hours=row["saturday_hours"],
            pto_hours=row["pto_hours"],
            total_hours=row["total_hours"],
            base_pay=row["base_pay"],
            overtime_pay=row["overtime_pay"],
            saturday_pay=row["saturday_pay"],
            gross_pay=row["gross_pay"],
            medical_deduction=row["medical_deduction"],
            total_employee_deductions=row["medical_deduction"],
            dependent_stipend=row["dependent_stipend"],
            taxable_income=row["taxable_income"],
            state_tax=row["state_tax"],
            federal_tax_employee=row["federal_tax_employee"],
            social_security_employee=row["social_security_employee"],
            medicare_employee=row["medicare_employee"],
            total_employee_taxes=row["total_employee_taxes"],
            net_pay=row["net_pay"],
            federal_tax_employer=row["federal_tax_employer"],
            social_security_employer=row["social_security_employer"],
            medicare_employer=row["medicare_employer"],
            total_employer_taxes=row["total_employer_taxes"],
            calculated_date=row["calculated_date"],
            period_start_date=period_start,
            period_end_date=period_end,
        )

        # Add optional employee name fields
        if first_name is not None:
            detail.first_name = first_name
        if last_name is not None:
            detail.last_name = last_name

        return detail

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "payroll_detail_id": self.payroll_detail_id,
            "payroll_id": self.payroll_id,
            "employee_id": self.employee_id,
            "hours": {
                "regular": self.regular_hours,
                "overtime": self.overtime_hours,
                "saturday": self.saturday_hours,
                "pto": self.pto_hours,
                "total": self.total_hours,
            },
            "pay": {
                "base": self.base_pay,
                "overtime": self.overtime_pay,
                "saturday": self.saturday_pay,
                "dependent_stipend": self.dependent_stipend,
                "gross": self.gross_pay,
            },
            "deductions": {
                "medical": self.medical_deduction,
            },
            "taxable_income": self.taxable_income,
            "employee_taxes": {
                "state": self.state_tax,
                "federal": self.federal_tax_employee,
                "social_security": self.social_security_employee,
                "medicare": self.medicare_employee,
                "total": self.total_employee_taxes,
            },
            "net_pay": self.net_pay,
            "employer_taxes": {
                "federal": self.federal_tax_employer,
                "social_security": self.social_security_employer,
                "medicare": self.medicare_employer,
                "total": self.total_employer_taxes,
            },
            "calculated_date": self.calculated_date,
        }

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"PayrollDetail(id={self.payroll_detail_id}, employee={self.employee_id}, "
            f"gross={self.gross_pay:.2f}, net={self.net_pay:.2f})"
        )


# =============================================================================
# PAYROLL CALCULATION HELPER CLASS
# =============================================================================


class PayrollCalculator:
    """
    Helper class for performing payroll calculations.

    Uses constants from src/utils/constants.py for all rates.
    """

    @staticmethod
    def calculate_hourly_pay(
        time_entries: list,
        hourly_rate: float,
    ) -> dict:
        """
        Calculate pay for an hourly employee based on time entries.

        Args:
            time_entries: List of TimeEntry objects for the pay period
            hourly_rate: Employee's hourly rate

        Returns:
            Dictionary with hours breakdown and pay amounts
        """
        regular_hours = 0.0
        overtime_hours = 0.0
        saturday_hours = 0.0
        pto_hours = 0.0

        # Sum up hours from all entries using daily overtime calculation
        for entry in time_entries:
            pto_hours += entry.pto_hours

            if entry.is_saturday:
                # All Saturday hours are at 1.5x
                saturday_hours += entry.hours_worked
            else:
                # Use entry's daily overtime calculation (over 8 hours/day)
                regular_hours += entry.regular_hours  # Up to 8 hours
                overtime_hours += entry.overtime_hours  # Hours over 8

        total_hours = regular_hours + overtime_hours + saturday_hours + pto_hours

        # Calculate pay
        base_pay = (regular_hours + pto_hours) * hourly_rate
        overtime_pay = overtime_hours * hourly_rate * OVERTIME_MULTIPLIER
        saturday_pay = saturday_hours * hourly_rate * SATURDAY_MULTIPLIER
        gross_pay = base_pay + overtime_pay + saturday_pay

        return {
            "regular_hours": regular_hours,
            "overtime_hours": overtime_hours,
            "saturday_hours": saturday_hours,
            "pto_hours": pto_hours,
            "total_hours": total_hours,
            "base_pay": round(base_pay, 2),
            "overtime_pay": round(overtime_pay, 2),
            "saturday_pay": round(saturday_pay, 2),
            "gross_pay": round(gross_pay, 2),
        }

    @staticmethod
    def calculate_salary_pay(annual_salary: float) -> dict:
        """
        Calculate weekly pay for a salaried employee.

        Args:
            annual_salary: Employee's annual salary

        Returns:
            Dictionary with hours and pay amounts
        """
        weekly_pay = annual_salary / WEEKS_PER_YEAR

        return {
            "regular_hours": STANDARD_WORK_HOURS_PER_WEEK,
            "overtime_hours": 0.0,
            "saturday_hours": 0.0,
            "pto_hours": 0.0,
            "total_hours": STANDARD_WORK_HOURS_PER_WEEK,
            "base_pay": round(weekly_pay, 2),
            "overtime_pay": 0.0,
            "saturday_pay": 0.0,
            "gross_pay": round(weekly_pay, 2),
        }

    @staticmethod
    def calculate_medical_deduction(medical_type: str) -> float:
        """
        Calculate weekly medical deduction.

        Args:
            medical_type: 'Single' or 'Family'

        Returns:
            Medical deduction amount
        """
        return (
            MEDICAL_DEDUCTION_FAMILY if medical_type == MEDICAL_TYPE_FAMILY
            else MEDICAL_DEDUCTION_SINGLE
        )

    @staticmethod
    def calculate_dependent_stipend(num_dependents: int) -> float:
        """
        Calculate dependent stipend (additional income per dependent).

        This is added to gross pay, not deducted from it.

        Args:
            num_dependents: Number of dependents

        Returns:
            Dependent stipend amount
        """
        return num_dependents * DEPENDENT_STIPEND_PER_DEPENDENT

    @staticmethod
    def calculate_taxes(taxable_income: float) -> dict:
        """
        Calculate all employee and employer taxes.

        Tax amounts are kept at full precision (4 decimal places) to avoid
        cumulative rounding errors. Only the final net pay should be rounded.
        
        NOTE: Uses flat 7.65% federal tax rate per project requirements.
        Progressive bracket calculation is available in _calculate_federal_tax_progressive()
        for future implementation.

        Args:
            taxable_income: Taxable income (gross pay - medical deduction)

        Returns:
            Dictionary with all tax amounts (4 decimal precision)
        """
        # Employee taxes (based on taxable income, not gross)
        # Keep full precision - round to 4 decimals to avoid floating point noise
        state_tax = round(taxable_income * STATE_TAX_RATE_IN, 4)

        # Federal tax uses flat 7.65% rate per project requirements
        federal_tax_employee = round(taxable_income * FEDERAL_TAX_RATE_EMPLOYEE, 4)

        social_security_employee = round(taxable_income * SOCIAL_SECURITY_RATE_EMPLOYEE, 4)
        medicare_employee = round(taxable_income * MEDICARE_RATE_EMPLOYEE, 4)
        total_employee_taxes = round(
            state_tax + federal_tax_employee + social_security_employee + medicare_employee,
            4
        )

        # Employer taxes (based on taxable income)
        federal_tax_employer = round(taxable_income * FEDERAL_TAX_RATE_EMPLOYER, 4)
        social_security_employer = round(taxable_income * SOCIAL_SECURITY_RATE_EMPLOYER, 4)
        medicare_employer = round(taxable_income * MEDICARE_RATE_EMPLOYER, 4)
        total_employer_taxes = round(
            federal_tax_employer + social_security_employer + medicare_employer,
            4
        )

        return {
            "state_tax": state_tax,
            "federal_tax_employee": federal_tax_employee,
            "social_security_employee": social_security_employee,
            "medicare_employee": medicare_employee,
            "total_employee_taxes": total_employee_taxes,
            "federal_tax_employer": federal_tax_employer,
            "social_security_employer": social_security_employer,
            "medicare_employer": medicare_employer,
            "total_employer_taxes": total_employer_taxes,
        }

    @staticmethod
    def calculate_net_pay(
        gross_pay: float,
        medical_deduction: float,
        total_employee_taxes: float,
    ) -> dict:
        """
        Calculate taxable income and net pay.

        Args:
            gross_pay: Gross pay (includes dependent stipend)
            medical_deduction: Medical deduction amount
            total_employee_taxes: Total employee taxes

        Returns:
            Dictionary with taxable income and net pay
        """
        # Taxable income = gross pay - medical deduction
        taxable_income = gross_pay - medical_deduction

        # Net pay = gross pay - medical deduction - taxes
        net_pay = taxable_income - total_employee_taxes

        # Use ROUND_HALF_UP for final currency values (traditional rounding)
        # Python's round() uses banker's rounding which rounds 0.5 to even
        def round_currency(value: float) -> float:
            """Round to 2 decimal places using traditional rounding (ROUND_HALF_UP)."""
            return float(Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

        return {
            "taxable_income": round_currency(taxable_income),
            "net_pay": round_currency(net_pay),
        }
