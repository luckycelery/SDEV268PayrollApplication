"""
User authentication and credential generation for payroll system
"""

import hashlib
import sqlite3
from datetime import datetime


def generate_employee_username(email: str) -> str:
    """
    Generate username from employee email

    Args:
        email: Employee email address (e.g., roy.mustang@abccompany.com)

    Returns:
        Username (e.g., roy.mustang)
    """
    return email.lower()


def generate_employee_password(email: str, dob: str) -> str:
    """
    Generate password from email + date of birth
    Format: <email_prefix><MMDDYYYY>

    Args:
        email: Employee email address
        dob: Date of birth in ISO format (YYYY-MM-DD)

    Returns:
        Generated password (e.g., roy.mustang11062005)

    Example:
        email = "roy.mustang@abccompany.com"
        dob = "2005-11-06"
        returns: "roy.mustang11062005"
    """
    username = email.split("@")[0].lower()
    # Convert YYYY-MM-DD to MMDDYYYY
    year, month, day = dob.split("-")
    formatted_dob = f"{month}{day}{year}"
    return f"{username}{formatted_dob}"


def hash_password(password: str) -> str:
    """
    Hash password using SHA256

    Note: Potentially upgrade to bcrypt

    Args:
        password: Plain text password

    Returns:
        Hashed password (hex string)
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash

    Args:
        plain_password: Password to check
        hashed_password: Stored hash

    Returns:
        True if password matches, False otherwise
    """
    return hash_password(plain_password) == hashed_password


def create_admin_account(conn: sqlite3.Connection, username: str = "HR0001", password: str = "AbccoTeam3") -> None:
    """
    Create admin user account

    Args:
        conn: SQLite database connection
        username: Admin username (default: HR0001)
        password: Admin password (default: AbccoTeam3)
    """
    cursor = conn.cursor()

    # Check if admin already exists
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        print(f"  WARNING: Admin user '{username}' already exists, skipping...")
        return

    password_hash = hash_password(password)
    cursor.execute(
        """
        INSERT INTO users (username, password_hash, user_type, employee_id, is_active)
        VALUES (?, ?, 'Admin', NULL, 1)
    """,
        (username, password_hash),
    )

    print(f"  Admin account created: {username}")


def create_employee_accounts(conn: sqlite3.Connection) -> int:
    """
    Create user accounts for all active employees

    Args:
        conn: SQLite database connection

    Returns:
        Number of employee accounts created
    """
    cursor = conn.cursor()

    # Get all active employees
    cursor.execute("""
        SELECT employee_id, email, date_of_birth
        FROM employees
        WHERE status = 'Active'
    """)

    employees = cursor.fetchall()
    created_count = 0

    for emp_id, email, dob in employees:
        username = generate_employee_username(email)
        password = generate_employee_password(email, dob)
        password_hash = hash_password(password)

        # Check if user already exists
        cursor.execute("SELECT user_id FROM users WHERE username = ? OR employee_id = ?", (username, emp_id))
        if cursor.fetchone():
            print(f"  WARNING: User for {emp_id} already exists, skipping...")
            continue

        cursor.execute(
            """
            INSERT INTO users (username, password_hash, user_type, employee_id, is_active)
            VALUES (?, ?, 'Employee', ?, 1)
        """,
            (username, password_hash, emp_id),
        )

        created_count += 1
        print(f"  Employee account created: {username} (Employee: {emp_id})")

    return created_count


def authenticate_user(
    conn: sqlite3.Connection, username: str, password: str
) -> tuple[str, str, str | None] | None:
    """
    Authenticate a user login attempt

    Args:
        conn: SQLite database connection
        username: Username attempting to log in
        password: Plain text password

    Returns:
        Tuple of (username, user_type, employee_id) if successful, None if failed
    """
    cursor = conn.cursor()

    # Use LOWER() for case-insensitive username matching
    cursor.execute(
        """
        SELECT username, password_hash, user_type, employee_id, is_active
        FROM users
        WHERE LOWER(username) = LOWER(?)
    """,
        (username,),
    )

    result = cursor.fetchone()

    if not result:
        return None  # User not found

    db_username, db_hash, user_type, employee_id, is_active = result

    if not is_active:
        return None  # Account disabled

    if not verify_password(password, db_hash):
        return None  # Wrong password

    # Update last login
    cursor.execute(
        """
        UPDATE users
        SET last_login = ?
        WHERE username = ?
    """,
        (datetime.now().isoformat(), username),
    )
    conn.commit()

    return (db_username, user_type, employee_id)


def setup_all_users(db_path: str) -> None:
    """
    Convenience function to set up all user accounts

    Args:
        db_path: Path to SQLite database
    """
    conn = sqlite3.connect(db_path)

    print("Creating user accounts...")

    # Create admin
    create_admin_account(conn)

    # Create employee accounts
    count = create_employee_accounts(conn)

    conn.commit()
    conn.close()

    print("\nUser setup complete!")
    print("   Admin accounts: 1")
    print(f"   Employee accounts: {count}")
    print("\nLogin credentials:")
    print("   Admin: HR0001 / AbccoTeam3")
    print("   Employees: <email_prefix><MMDDYYYY>")


if __name__ == "__main__":
    # Test authentication
    db_path = "payroll.db"
    setup_all_users(db_path)

    # Test login
    print("\nTesting authentication...")
    conn = sqlite3.connect(db_path)

    # Test admin login
    result = authenticate_user(conn, "HR0001", "AbccoTeam3")
    if result:
        print(f"Admin login successful: {result}")
    else:
        print("Admin login failed")

    # Test employee login
    result = authenticate_user(conn, "roy.mustang", "roy.mustang11062005")
    if result:
        print(f"Employee login successful: {result}")
    else:
        print("Employee login failed")

    conn.close()
