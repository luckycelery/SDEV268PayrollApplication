"""
Load Sample Time Entries from CSV

This script loads time entry data from a CSV file into the database.
Uses direct SQL with a single connection for efficiency.

Usage:
    uv run python load_time_entries.py [csv_file]

    If no csv_file is specified, defaults to data/sample_time_entries.csv

CSV Format:
    employee_id,work_date,hours_worked,pto_hours
    E001,2025-11-18,8.0,0
    E001,2025-11-19,0,8.0  (PTO day)
"""

import csv
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

DB_PATH = "../../payroll.db"


def get_day_of_week(date_str: str) -> str:
    """Get day name from date string."""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%A")


def is_saturday(date_str: str) -> int:
    """Check if date is Saturday (returns 1 or 0)."""
    return 1 if get_day_of_week(date_str) == "Saturday" else 0


def main():
    """Main entry point."""
    # Determine CSV file path
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "../../data/sample_time_entries.csv"

    if not Path(csv_path).exists():
        print(f"Error: File not found: {csv_path}")
        sys.exit(1)

    print("=" * 60)
    print("Loading Sample Time Entries")
    print("=" * 60)

    # Use a SINGLE connection for everything
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Step 1: Initialize PTO balances for ALL employees (including terminated for historical data)
    print("\n[1] Initializing PTO Balances (40 hours each)...")
    cursor.execute(
        """
        SELECT e.employee_id
        FROM employees e
        LEFT JOIN pto_balances p ON e.employee_id = p.employee_id
        WHERE p.employee_id IS NULL
        """
    )
    employees_needing_pto = cursor.fetchall()
    pto_created = 0

    for (emp_id,) in employees_needing_pto:
        cursor.execute(
            """
            INSERT INTO pto_balances (employee_id, total_accrued, total_used, balance)
            VALUES (?, 40.0, 0, 40.0)
            """,
            (emp_id,),
        )
        pto_created += 1
        print(f"  Created PTO balance for {emp_id}: 40.0 hours")

    conn.commit()
    print(f"    Created {pto_created} new PTO balance records")

    # Step 2: Load time entries
    print(f"\n[2] Loading time entries from: {csv_path}")

    success_count = 0
    skip_count = 0
    errors = []

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)

        for row_num, row in enumerate(reader, start=2):
            # Skip comment lines
            if row["employee_id"].startswith("#"):
                continue

            try:
                employee_id = row["employee_id"].strip()
                work_date = row["work_date"].strip()
                hours_worked = float(row["hours_worked"].strip())
                pto_hours = float(row["pto_hours"].strip())

                # Skip if no hours at all
                if hours_worked == 0 and pto_hours == 0:
                    skip_count += 1
                    continue

                # Check if entry already exists
                cursor.execute(
                    "SELECT 1 FROM time_entries WHERE employee_id = ? AND entry_date = ?",
                    (employee_id, work_date),
                )
                if cursor.fetchone():
                    print(f"  Skipping row {row_num}: Entry already exists for {employee_id} on {work_date}")
                    skip_count += 1
                    continue

                # Validate employee exists
                cursor.execute(
                    "SELECT 1 FROM employees WHERE employee_id = ?",
                    (employee_id,),
                )
                if not cursor.fetchone():
                    errors.append(f"Row {row_num}: Employee {employee_id} not found")
                    continue

                # Calculate day info
                day_name = get_day_of_week(work_date)
                is_sat = is_saturday(work_date)

                # Insert time entry
                cursor.execute(
                    """
                    INSERT INTO time_entries (
                        employee_id, entry_date, day_of_week,
                        hours_worked, pto_hours, is_saturday
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (employee_id, work_date, day_name, hours_worked, pto_hours, is_sat),
                )
                success_count += 1

            except KeyError as e:
                errors.append(f"Row {row_num}: Missing column {e}")
            except ValueError as e:
                errors.append(f"Row {row_num}: Invalid value - {e}")
            except Exception as e:
                errors.append(f"Row {row_num}: {e}")

    # Commit all inserts
    conn.commit()
    conn.close()

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Time entries created: {success_count}")
    print(f"  Entries skipped:      {skip_count}")
    print(f"  Errors:               {len(errors)}")

    if errors:
        print("\nErrors encountered:")
        for error in errors[:10]:
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")

    print("\nDone!")


if __name__ == "__main__":
    main()
