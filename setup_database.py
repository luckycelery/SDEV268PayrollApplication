"""
One-command database initialization script
Run this to create a fresh database with sample data and user accounts
"""

import sqlite3
import sys
from pathlib import Path

# Add database directory to path
sys.path.insert(0, str(Path(__file__).parent / "database"))

from auth import setup_all_users
from load_test_data import load_sample_data


def setup_database():
    """Initialize complete database with schema, data, and users"""

    DB_PATH = "payroll.db"
    SCHEMA_PATH = "database/schema.sql"
    DATA_PATH = "database/sample_data.json"

    # Check if database exists
    if Path(DB_PATH).exists():
        print(f"WARNING: Database '{DB_PATH}' already exists!")
        response = input("Delete and recreate? (yes/no): ").strip().lower()
        if response != "yes":
            print("Setup cancelled.")
            return
        Path(DB_PATH).unlink()
        print("Deleted existing database\n")

    print("=" * 60)
    print("ABC COMPANY PAYROLL SYSTEM - DATABASE SETUP")
    print("=" * 60)

    # Step 1: Create schema
    print("\n[1] Creating database schema...")
    try:
        conn = sqlite3.connect(DB_PATH)
        with open(SCHEMA_PATH, "r") as f:
            conn.executescript(f.read())
        conn.close()
        print("   Schema created successfully")
    except Exception as e:
        print(f"   ERROR: Schema creation failed: {e}")
        return

    # Step 2: Load sample data
    print("\n[2] Loading sample employee data...")
    try:
        load_sample_data(DB_PATH, DATA_PATH)
    except Exception as e:
        print(f"   ERROR: Data loading failed: {e}")
        return

    # Step 3: Create user accounts
    print("\n[3] Creating user accounts...")
    try:
        setup_all_users(DB_PATH)
    except Exception as e:
        print(f"   ERROR: User creation failed: {e}")
        return

    # Success summary
    print("\n" + "=" * 60)
    print("DATABASE SETUP COMPLETE!")
    print("=" * 60)
    print(f"\nDatabase file: {DB_PATH}")
    print(f"Schema: {SCHEMA_PATH}")
    print(f"Sample data: {DATA_PATH}")

    print("\nLOGIN CREDENTIALS:")
    print("   Admin:")
    print("     Username: HR0001")
    print("     Password: AbccoTeam3")
    print("\n   Employees:")
    print("     Username: <email_prefix>")
    print("     Password: <email_prefix><MMDDYYYY>")
    print("     Example: roy.mustang / roy.mustang11062005")

    print("\nNEXT STEPS:")
    print("   1. Test database: python -m database.auth")
    print("   2. Start GUI development (Week 5)")
    print("   3. Share DB with team: git push")
    print("=" * 60)


if __name__ == "__main__":
    setup_database()
    print("Sample data loaded successfully!")
