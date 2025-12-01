"""
TimeEntry Model - Represents daily time entry records for employees
Matches the time_entries table in database/schema.sql
"""

import sqlite3
from datetime import datetime
from typing import Optional

from src.utils.constants import (
    DAYS_OF_WEEK,
    MAX_HOURS_PER_DAY,
    MAX_PTO_HOURS_PER_DAY,
    OVERTIME_THRESHOLD_DAILY,
)

from .base_model import BaseModel


class TimeEntry(BaseModel):
    """
    TimeEntry model - handles daily time tracking for employees

    Matches the database schema:
    - time_entries table: Daily records of hours worked and PTO used
    - Links to employees and payroll_periods tables
    """

    def __init__(
        self,
        employee_id: str,
        entry_date: str,
        day_of_week: str,
        # Optional fields with defaults
        time_entry_id: int | None = None,
        payroll_id: int | None = None,
        hours_worked: float = 0.0,
        pto_hours: float = 0.0,
        is_saturday: int = 0,
        notes: str | None = None,
        created_date: str | None = None,
        modified_date: str | None = None,
    ):
        """
        Initialize TimeEntry object matching database schema.

        Args:
            employee_id: Employee ID (FK to employees table)
            entry_date: Date of entry (YYYY-MM-DD format)
            day_of_week: Day name (Monday, Tuesday, etc.)
            time_entry_id: Auto-generated primary key
            payroll_id: FK to payroll_periods (NULL until assigned)
            hours_worked: Hours worked this day (0-24)
            pto_hours: PTO hours used this day (0-8)
            is_saturday: 1 if Saturday (all hours at 1.5x), 0 otherwise
            notes: Optional admin notes
            created_date: Timestamp of record creation
            modified_date: Timestamp of last modification
        """
        self.time_entry_id = time_entry_id
        self.employee_id = employee_id
        self.payroll_id = payroll_id
        self.entry_date = entry_date
        self.day_of_week = day_of_week
        self.hours_worked = hours_worked
        self.pto_hours = pto_hours
        self.is_saturday = is_saturday
        self.notes = notes
        self.created_date = created_date
        self.modified_date = modified_date

    # =========================================================================
    # PROPERTIES
    # =========================================================================

    @property
    def total_hours(self) -> float:
        """Total hours for this day (worked + PTO)."""
        return self.hours_worked + self.pto_hours

    @property
    def overtime_hours(self) -> float:
        """Hours over 8 for this day (daily overtime)."""
        if self.hours_worked > OVERTIME_THRESHOLD_DAILY:
            return self.hours_worked - OVERTIME_THRESHOLD_DAILY
        return 0.0

    @property
    def regular_hours(self) -> float:
        """Regular hours (up to 8) for this day."""
        return min(self.hours_worked, OVERTIME_THRESHOLD_DAILY)

    @property
    def is_saturday_bool(self) -> bool:
        """Return is_saturday as boolean."""
        return self.is_saturday == 1

    # =========================================================================
    # VALIDATION
    # =========================================================================

    def validate(self) -> list[str]:
        """
        Validate time entry data.

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        # Validate employee_id
        if not self.employee_id or not self.employee_id.strip():
            errors.append("Employee ID is required")

        # Validate entry_date
        if not self.entry_date:
            errors.append("Entry date is required")
        else:
            try:
                datetime.strptime(self.entry_date, "%Y-%m-%d")
            except ValueError:
                errors.append("Entry date must be in YYYY-MM-DD format")

        # Validate day_of_week
        if self.day_of_week not in DAYS_OF_WEEK:
            errors.append(f"Day of week must be one of: {', '.join(DAYS_OF_WEEK)}")

        # Validate hours_worked
        if self.hours_worked < 0:
            errors.append("Hours worked cannot be negative")
        if self.hours_worked > MAX_HOURS_PER_DAY:
            errors.append(f"Hours worked cannot exceed {MAX_HOURS_PER_DAY}")

        # Validate pto_hours
        if self.pto_hours < 0:
            errors.append("PTO hours cannot be negative")
        if self.pto_hours > MAX_PTO_HOURS_PER_DAY:
            errors.append(f"PTO hours cannot exceed {MAX_PTO_HOURS_PER_DAY}")

        # Validate total hours
        if self.total_hours > MAX_HOURS_PER_DAY:
            errors.append(f"Total hours (worked + PTO) cannot exceed {MAX_HOURS_PER_DAY}")

        # Validate is_saturday consistency
        if self.day_of_week == "Saturday" and self.is_saturday != 1:
            errors.append("is_saturday must be 1 for Saturday entries")

        return errors

    def is_valid(self) -> bool:
        """Check if time entry data is valid."""
        return len(self.validate()) == 0

    # =========================================================================
    # DATABASE OPERATIONS - CREATE
    # =========================================================================

    def save(self) -> bool:
        """
        Save time entry to database (insert or update).

        Returns:
            True if save was successful, False otherwise
        """
        if not self.is_valid():
            return False

        if self.time_entry_id is None:
            return self._insert()
        else:
            return self._update()

    def _insert(self) -> bool:
        """Insert new time entry record."""
        query = """
            INSERT INTO time_entries (
                employee_id, payroll_id, entry_date, day_of_week,
                hours_worked, pto_hours, is_saturday, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            self.employee_id,
            self.payroll_id,
            self.entry_date,
            self.day_of_week,
            self.hours_worked,
            self.pto_hours,
            self.is_saturday,
            self.notes,
        )

        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            self.time_entry_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # Likely duplicate entry for same employee/date
            return False

    def _update(self) -> bool:
        """Update existing time entry record."""
        query = """
            UPDATE time_entries SET
                employee_id = ?,
                payroll_id = ?,
                entry_date = ?,
                day_of_week = ?,
                hours_worked = ?,
                pto_hours = ?,
                is_saturday = ?,
                notes = ?
            WHERE time_entry_id = ?
        """
        params = (
            self.employee_id,
            self.payroll_id,
            self.entry_date,
            self.day_of_week,
            self.hours_worked,
            self.pto_hours,
            self.is_saturday,
            self.notes,
            self.time_entry_id,
        )

        affected = self.execute_write(query, params)
        return affected > 0

    # =========================================================================
    # DATABASE OPERATIONS - READ
    # =========================================================================

    @classmethod
    def get_by_id(cls, time_entry_id: int) -> Optional["TimeEntry"]:
        """
        Retrieve time entry by ID.

        Args:
            time_entry_id: Primary key of time entry

        Returns:
            TimeEntry object or None if not found
        """
        query = "SELECT * FROM time_entries WHERE time_entry_id = ?"
        row = cls.execute_single(query, (time_entry_id,))

        if row is None:
            return None

        return cls._row_to_time_entry(row)

    @classmethod
    def get_by_employee_and_date(
        cls, employee_id: str, entry_date: str
    ) -> Optional["TimeEntry"]:
        """
        Retrieve time entry for specific employee and date.

        Args:
            employee_id: Employee ID
            entry_date: Date in YYYY-MM-DD format

        Returns:
            TimeEntry object or None if not found
        """
        query = """
            SELECT * FROM time_entries
            WHERE employee_id = ? AND entry_date = ?
        """
        row = cls.execute_single(query, (employee_id, entry_date))

        if row is None:
            return None

        return cls._row_to_time_entry(row)

    @classmethod
    def get_by_employee(
        cls,
        employee_id: str,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list["TimeEntry"]:
        """
        Get all time entries for an employee, optionally within date range.

        Args:
            employee_id: Employee ID
            start_date: Optional start date filter (inclusive)
            end_date: Optional end date filter (inclusive)

        Returns:
            List of TimeEntry objects ordered by date
        """
        if start_date and end_date:
            query = """
                SELECT * FROM time_entries
                WHERE employee_id = ?
                AND entry_date >= ? AND entry_date <= ?
                ORDER BY entry_date
            """
            params = (employee_id, start_date, end_date)
        elif start_date:
            query = """
                SELECT * FROM time_entries
                WHERE employee_id = ? AND entry_date >= ?
                ORDER BY entry_date
            """
            params = (employee_id, start_date)
        elif end_date:
            query = """
                SELECT * FROM time_entries
                WHERE employee_id = ? AND entry_date <= ?
                ORDER BY entry_date
            """
            params = (employee_id, end_date)
        else:
            query = """
                SELECT * FROM time_entries
                WHERE employee_id = ?
                ORDER BY entry_date
            """
            params = (employee_id,)

        rows = cls.execute_query(query, params)
        return [cls._row_to_time_entry(row) for row in rows]

    @classmethod
    def get_by_payroll(cls, payroll_id: int) -> list["TimeEntry"]:
        """
        Get all time entries for a payroll period.

        Args:
            payroll_id: Payroll period ID

        Returns:
            List of TimeEntry objects
        """
        query = """
            SELECT * FROM time_entries
            WHERE payroll_id = ?
            ORDER BY employee_id, entry_date
        """
        rows = cls.execute_query(query, (payroll_id,))
        return [cls._row_to_time_entry(row) for row in rows]

    @classmethod
    def get_unassigned_entries(
        cls, employee_id: str, start_date: str, end_date: str
    ) -> list["TimeEntry"]:
        """
        Get time entries not yet assigned to a payroll period.

        Args:
            employee_id: Employee ID
            start_date: Period start date
            end_date: Period end date

        Returns:
            List of unassigned TimeEntry objects
        """
        query = """
            SELECT * FROM time_entries
            WHERE employee_id = ?
            AND entry_date >= ? AND entry_date <= ?
            AND payroll_id IS NULL
            ORDER BY entry_date
        """
        rows = cls.execute_query(query, (employee_id, start_date, end_date))
        return [cls._row_to_time_entry(row) for row in rows]

    # =========================================================================
    # DATABASE OPERATIONS - UPDATE
    # =========================================================================

    @classmethod
    def assign_to_payroll(
        cls, employee_id: str, start_date: str, end_date: str, payroll_id: int
    ) -> int:
        """
        Assign time entries to a payroll period.

        Args:
            employee_id: Employee ID
            start_date: Period start date
            end_date: Period end date
            payroll_id: Payroll period ID to assign

        Returns:
            Number of entries updated
        """
        query = """
            UPDATE time_entries
            SET payroll_id = ?
            WHERE employee_id = ?
            AND entry_date >= ? AND entry_date <= ?
            AND payroll_id IS NULL
        """
        return cls.execute_write(query, (payroll_id, employee_id, start_date, end_date))

    # =========================================================================
    # DATABASE OPERATIONS - DELETE
    # =========================================================================

    def delete(self) -> bool:
        """
        Delete this time entry from database.

        Returns:
            True if deletion was successful
        """
        if self.time_entry_id is None:
            return False

        query = "DELETE FROM time_entries WHERE time_entry_id = ?"
        affected = self.execute_write(query, (self.time_entry_id,))
        return affected > 0

    @classmethod
    def delete_by_id(cls, time_entry_id: int) -> bool:
        """
        Delete time entry by ID.

        Args:
            time_entry_id: Primary key of time entry

        Returns:
            True if deletion was successful
        """
        query = "DELETE FROM time_entries WHERE time_entry_id = ?"
        affected = cls.execute_write(query, (time_entry_id,))
        return affected > 0

    # =========================================================================
    # HELPER METHODS
    # =========================================================================

    @classmethod
    def _row_to_time_entry(cls, row: sqlite3.Row) -> "TimeEntry":
        """Convert database row to TimeEntry object."""
        return TimeEntry(
            time_entry_id=row["time_entry_id"],
            employee_id=row["employee_id"],
            payroll_id=row["payroll_id"],
            entry_date=row["entry_date"],
            day_of_week=row["day_of_week"],
            hours_worked=row["hours_worked"],
            pto_hours=row["pto_hours"],
            is_saturday=row["is_saturday"],
            notes=row["notes"],
            created_date=row["created_date"],
            modified_date=row["modified_date"],
        )

    @classmethod
    def get_day_of_week(cls, date_str: str) -> str:
        """
        Get day of week name from date string.

        Args:
            date_str: Date in YYYY-MM-DD format

        Returns:
            Day name (Monday, Tuesday, etc.)
        """
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return DAYS_OF_WEEK[date_obj.weekday()]

    @classmethod
    def create_entry(
        cls,
        employee_id: str,
        entry_date: str,
        hours_worked: float = 0.0,
        pto_hours: float = 0.0,
        notes: str | None = None,
    ) -> "TimeEntry":
        """
        Factory method to create a new TimeEntry with computed fields.

        Args:
            employee_id: Employee ID
            entry_date: Date in YYYY-MM-DD format
            hours_worked: Hours worked
            pto_hours: PTO hours used
            notes: Optional notes

        Returns:
            New TimeEntry object (not saved to database)
        """
        day_of_week = cls.get_day_of_week(entry_date)
        is_saturday = 1 if day_of_week == "Saturday" else 0

        return TimeEntry(
            employee_id=employee_id,
            entry_date=entry_date,
            day_of_week=day_of_week,
            hours_worked=hours_worked,
            pto_hours=pto_hours,
            is_saturday=is_saturday,
            notes=notes,
        )

    def to_dict(self) -> dict:
        """
        Convert TimeEntry to dictionary.

        Returns:
            Dictionary representation of time entry
        """
        return {
            "time_entry_id": self.time_entry_id,
            "employee_id": self.employee_id,
            "payroll_id": self.payroll_id,
            "entry_date": self.entry_date,
            "day_of_week": self.day_of_week,
            "hours_worked": self.hours_worked,
            "pto_hours": self.pto_hours,
            "is_saturday": self.is_saturday,
            "notes": self.notes,
            "total_hours": self.total_hours,
            "regular_hours": self.regular_hours,
            "overtime_hours": self.overtime_hours,
            "created_date": self.created_date,
            "modified_date": self.modified_date,
        }

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"TimeEntry(id={self.time_entry_id}, employee={self.employee_id}, "
            f"date={self.entry_date}, hours={self.hours_worked}, pto={self.pto_hours})"
        )
