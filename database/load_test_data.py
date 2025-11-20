"""
Load sample employee data from JSON into SQLite database
"""

import json
import sqlite3
from pathlib import Path


def load_sample_data(db_path: str, json_path: str) -> None:
    """
    Load departments, job titles, employees, and compensation from JSON file

    Args:
        db_path: Path to SQLite database file
        json_path: Path to JSON file with sample data
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Load JSON data
    with open(json_path, "r") as f:
        data = json.load(f)

    print("Loading sample data...")

    # 1. Load departments
    print(f"  Loading {len(data['departments'])} departments...")
    for dept in data["departments"]:
        cursor.execute("INSERT INTO departments (department_name) VALUES (?)", (dept["department_name"],))

    # 2. Load job titles
    print(f"  Loading {len(data['job_titles'])} job titles...")
    for title in data["job_titles"]:
        cursor.execute("INSERT INTO job_titles (title_name) VALUES (?)", (title["title_name"],))

    # 3. Build lookup maps for foreign keys
    cursor.execute("SELECT department_id, department_name FROM departments")
    dept_map = {name: id for id, name in cursor.fetchall()}

    cursor.execute("SELECT job_title_id, title_name FROM job_titles")
    title_map = {name: id for id, name in cursor.fetchall()}

    # 4. Load employees
    print(f"  Loading {len(data['employees'])} employees...")
    for emp in data["employees"]:
        # Convert department/title names to IDs
        dept_id = dept_map[emp.pop("department_name")]
        title_id = title_map[emp.pop("job_title_name")]

        cursor.execute(
            """
            INSERT INTO employees (
                employee_id, first_name, last_name, surname, date_of_birth,
                gender, email, address_line1, address_line2, city, state,
                zip_code, has_picture, picture_filename, status, date_hired,
                department_id, job_title_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                emp["employee_id"],
                emp["first_name"],
                emp["last_name"],
                emp["surname"],
                emp["date_of_birth"],
                emp["gender"],
                emp["email"],
                emp["address_line1"],
                emp["address_line2"],
                emp["city"],
                emp["state"],
                emp["zip_code"],
                emp["has_picture"],
                emp["picture_filename"],
                emp["status"],
                emp["date_hired"],
                dept_id,
                title_id,
            ),
        )

    # 5. Load compensation
    print(f"  Loading {len(data['compensation'])} compensation records...")
    for comp in data["compensation"]:
        cursor.execute(
            """
            INSERT INTO compensation (
                employee_id, salary_type, base_salary, hourly_rate,
                medical_type, num_dependents, effective_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                comp["employee_id"],
                comp["salary_type"],
                comp["base_salary"],
                comp["hourly_rate"],
                comp["medical_type"],
                comp["num_dependents"],
                comp["effective_date"],
            ),
        )

    # 6. Initialize PTO balances for active employees
    print("  Initializing PTO balances...")
    cursor.execute("""
        INSERT INTO pto_balances (employee_id, total_accrued, total_used, balance)
        SELECT employee_id, 40.0, 0.0, 40.0
        FROM employees
        WHERE status = 'Active'
    """)

    conn.commit()
    print("Sample data loaded successfully!")
    print(f"   Total employees: {len(data['employees'])}")
    print(
        f"   Active employees: {cursor.execute('SELECT COUNT(*) FROM employees WHERE status = ?', ('Active',)).fetchone()[0]}"
    )

    conn.close()


if __name__ == "__main__":
    # Test the function
    db_path = "payroll.db"
    json_path = "database/sample_data.json"

    if Path(db_path).exists():
        print(f"WARNING: Database {db_path} already exists!")
        response = input("Delete and recreate? (yes/no): ")
        if response.lower() != "yes":
            print("Aborted.")
            exit(0)
        Path(db_path).unlink()

    # Create schema
    print("Creating database schema...")
    conn = sqlite3.connect(db_path)
    with open("database/schema.sql", "r") as f:
        conn.executescript(f.read())
    conn.close()

    # Load data
    load_sample_data(db_path, json_path)
