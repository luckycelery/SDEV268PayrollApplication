"""
One-command database setup script
Runs schema creation, data loading, and user account creation
"""
import sqlite3
import sys
from pathlib import Path

from constants import DB_PATH, LINE_LENGTH, PROJECT_ROOT, SAMPLE_DATA_FILE, SCHEMA_FILE

sys.path.insert(0, str(PROJECT_ROOT))

from database.auth import setup_all_users
from database.load_data import load_test_data


def run_sql_file(db_path: Path, sql_file: Path) -> None:
    """Execute SQL file against database"""
    print(f"\nExecuting {sql_file.name}...")

    with open(sql_file) as f:
        sql_script = f.read()

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    try:
        cursor.executescript(sql_script)
        conn.commit()
        print("  [OK] Schema created successfully")
    except Exception as e:
        print(f"  [FAIL] Error creating schema: {e}")
        sys.exit(1)
    finally:
        conn.close()


def main():
    """Main setup function"""
    # Configuration from constants
    db_path = DB_PATH
    schema_file = SCHEMA_FILE
    data_file = SAMPLE_DATA_FILE

    print("=" * LINE_LENGTH)
    print("PAYROLL DATABASE SETUP")
    print("=" * LINE_LENGTH)
    print("\nThis script will:")
    print("  1. Create database schema")
    print("  2. Load test data (with validation)")
    print("  3. Create user accounts")
    print("=" * LINE_LENGTH)

    # Check if database already exists
    if db_path.exists():
        response = input(f"\n[WARNING] {db_path} already exists. Delete and recreate? (yes/no): ")
        if response.lower() != 'yes':
            print("Setup cancelled.")
            return
        db_path.unlink()
        print("[OK] Deleted existing database")

    # Step 1: Create schema
    print("\n" + "=" * LINE_LENGTH)
    print("STEP 1: CREATING DATABASE SCHEMA")
    print("=" * LINE_LENGTH)
    run_sql_file(db_path, schema_file)

    # Step 2: Load test data
    print("\n" + "=" * LINE_LENGTH)
    print("STEP 2: LOADING TEST DATA")
    print("=" * LINE_LENGTH)
    print("Loading data with graceful error handling...")
    print("Valid records will be loaded, invalid records will be reported.\n")

    report = load_test_data(str(db_path), str(data_file))
    report.print_summary()

    # Step 3: Create user accounts
    print("\n" + "=" * LINE_LENGTH)
    print("STEP 3: CREATING USER ACCOUNTS")
    print("=" * LINE_LENGTH)

    setup_all_users(str(db_path))

    # Final summary
    print("\n" + "=" * LINE_LENGTH)
    print("SETUP COMPLETE!")
    print("=" * LINE_LENGTH)

    # Verify database
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM employees WHERE status = 'Active'")
    active_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE user_type = 'Employee'")
    user_count = cursor.fetchone()[0]

    conn.close()

    print("\nDatabase Statistics:")
    print(f"  Active employees: {active_count}")
    print(f"  Employee user accounts: {user_count}")
    print("  Admin accounts: 1")

    if len(report.employees_failed) > 0:
        print(f"\n[INFO] {len(report.employees_failed)} employee(s) failed validation")


if __name__ == "__main__":
    main()
