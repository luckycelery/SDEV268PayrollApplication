"""
Basic test script for payroll database
Verifies database setup completed successfully
"""

import sqlite3
import sys
from pathlib import Path


def test_database():
    """Run basic database validation tests"""
    db_path = "payroll.db"

    print("\n" + "=" * 60)
    print("ABC COMPANY PAYROLL SYSTEM - DATABASE VALIDATION")
    print("=" * 60)

    # Test 1: Database file exists
    print("\n[1] Checking database file...")
    if not Path(db_path).exists():
        print("    ERROR: Database file not found")
        print("    Run: python setup_database.py")
        return False
    print(f"    OK: {db_path} exists")

    # Connect to database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
    except Exception as e:
        print(f"    ERROR: Cannot connect to database: {e}")
        return False

    # Test 2: Required tables exist
    print("\n[2] Checking required tables...")
    required_tables = [
        "departments",
        "job_titles",
        "employees",
        "compensation",
        "users",
        "payroll_periods",
        "time_entries",
        "pto_balances",
        "payroll_details",
    ]

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = [row[0] for row in cursor.fetchall()]

    missing = [t for t in required_tables if t not in existing_tables]
    if missing:
        print(f"    ERROR: Missing tables: {', '.join(missing)}")
        conn.close()
        return False
    print(f"    OK: All {len(required_tables)} tables exist")

    # Test 3: Sample data loaded
    print("\n[3] Checking sample data...")
    counts = {}
    for table in ["departments", "job_titles", "employees", "compensation"]:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        counts[table] = cursor.fetchone()[0]

    if any(count == 0 for count in counts.values()):
        print("    ERROR: Some tables are empty")
        for table, count in counts.items():
            print(f"      {table}: {count} records")
        conn.close()
        return False

    print("    OK: Sample data loaded")
    for table, count in counts.items():
        print(f"      {table}: {count} records")

    # Test 4: User accounts exist
    print("\n[4] Checking user accounts...")
    cursor.execute("SELECT COUNT(*) FROM users WHERE username='HR0001'")
    admin_exists = cursor.fetchone()[0] > 0

    cursor.execute("SELECT COUNT(*) FROM users WHERE user_type='Employee'")
    employee_count = cursor.fetchone()[0]

    if not admin_exists:
        print("    ERROR: Admin account not found")
        conn.close()
        return False

    print("    OK: Admin account exists")
    print(f"    OK: {employee_count} employee accounts created")

    # Test 5: Basic authentication
    print("\n[5] Testing authentication...")
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        from auth import authenticate_user

        result = authenticate_user(conn, "HR0001", "AbccoTeam3")
        if not result or result[1] != "Admin":
            print("    ERROR: Admin login failed")
            conn.close()
            return False
        print("    OK: Admin login works (HR0001 / AbccoTeam3)")
    except Exception as e:
        print(f"    ERROR: Authentication test failed: {e}")
        conn.close()
        return False

    conn.close()

    # Success
    print("\n" + "=" * 60)
    print("DATABASE VALIDATION PASSED")
    print("=" * 60)
    print("\nDatabase is ready for use!")
    print("\nNext steps:")
    print("  - Begin GUI development")
    print("  - Implement payroll calculations")
    print("  - Add additional features as needed")
    print()

    return True


if __name__ == "__main__":
    success = test_database()
    sys.exit(0 if success else 1)
