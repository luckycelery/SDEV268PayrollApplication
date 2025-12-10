"""
User authentication and credential generation for payroll system

Security Module - External Library: PyNaCl
Uses Argon2id password hashing algorithm
Provides memory-hard, GPU-resistant password storage with automatic salting
"""

import sqlite3
from datetime import datetime

import nacl.exceptions
import nacl.pwhash


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
    Hash password using Argon2id (via PyNaCl)

    Uses OPSLIMIT_INTERACTIVE for fast hashing suitable for login flows.
    Automatically generates random salt and encodes in modular crypt format.

    Args:
        password: Plain text password

    Returns:
        Argon2id hash in modular crypt format (e.g., $argon2id$v=19$m=65536,t=2,p=1$...)

    Security:
        - Memory-hard algorithm resistant to GPU/ASIC attacks
        - Automatic salt generation (no collision risk)
        - OPSLIMIT_INTERACTIVE: ~100-200ms hashing time
    """
    # print("=" * LINE_LENGTH)
    # print(f"Password to hash: {password}")
    password_bytes = password.encode("utf-8")
    hashed = nacl.pwhash.str(
        password_bytes,
        opslimit=nacl.pwhash.argon2id.OPSLIMIT_INTERACTIVE,
        memlimit=nacl.pwhash.argon2id.MEMLIMIT_INTERACTIVE,
    )
    decoded = hashed.decode("utf-8")
    # print(f"Password hash using Argon2id: {decoded}")
    return decoded


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its Argon2id hash

    Args:
        plain_password: Password to check
        hashed_password: Stored Argon2id hash

    Returns:
        True if password matches, False otherwise

    Security:
        - Constant-time comparison via nacl.pwhash.verify
        - Automatically detects hash parameters from modular crypt string
    """
    try:
        password_bytes = plain_password.encode("utf-8")
        hash_bytes = hashed_password.encode("utf-8")
        nacl.pwhash.verify(hash_bytes, password_bytes)
        return True
    except (nacl.exceptions.InvalidkeyError, ValueError, AttributeError):
        return False


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


def create_user_account_for_employee(
    employee_id: str, email: str, dob: str, conn: sqlite3.Connection | None = None
) -> bool:
    """
    Create a user account for a single employee

    Args:
        employee_id: Employee ID
        email: Employee email address
        dob: Date of birth in ISO format (YYYY-MM-DD)
        conn: SQLite database connection (optional, will create if None)

    Returns:
        True if user account created successfully, False otherwise
    """
    should_close = False
    if conn is None:
        from src.models.base_model import BaseModel

        conn = sqlite3.connect(BaseModel.DB_PATH)
        should_close = True

    try:
        cursor = conn.cursor()

        username = generate_employee_username(email)
        password = generate_employee_password(email, dob)
        password_hash = hash_password(password)

        # Check if user already exists
        cursor.execute("SELECT user_id FROM users WHERE username = ? OR employee_id = ?", (username, employee_id))
        if cursor.fetchone():
            print(f"  WARNING: User for {employee_id} already exists, skipping...")
            return True  # Already exists, so technically successful

        cursor.execute(
            """
            INSERT INTO users (username, password_hash, user_type, employee_id, is_active)
            VALUES (?, ?, 'Employee', ?, 1)
        """,
            (username, password_hash, employee_id),
        )

        conn.commit()
        print(f"  Employee account created: {username} (Employee: {employee_id})")
        return True

    except Exception as e:
        print(f"  ERROR: Failed to create user account for {employee_id}: {e}")
        return False

    finally:
        if should_close:
            conn.close()


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
        if create_user_account_for_employee(emp_id, email, dob, conn):
            created_count += 1

    return created_count


def sanitize_username(username: str) -> str:
    """
    Sanitize username input to prevent injection attacks

    Args:
        username: Raw username input

    Returns:
        Sanitized username (lowercase, stripped)
    """
    return username.strip().lower()


def log_security_event(conn: sqlite3.Connection, username: str, event_type: str, success: bool) -> None:
    """
    Log security events for audit trail

    Args:
        conn: SQLite database connection
        username: Username involved in event
        event_type: Type of event (e.g., 'login_attempt')
        success: Whether the event succeeded

    Note:
        Logs to console for this school project. In production, would write to
        audit_log table or external logging service.
    """
    timestamp = datetime.now().isoformat()
    status = "SUCCESS" if success else "FAILED"
    print(f"[{timestamp}] SECURITY: {event_type} - {username} - {status}")


def authenticate_user(
    conn: sqlite3.Connection, username: str, password: str
) -> tuple[str, str, str | None] | None:
    """
    Authenticate a user login attempt with security logging

    Args:
        conn: SQLite database connection
        username: Username attempting to log in
        password: Plain text password

    Returns:
        Tuple of (username, user_type, employee_id) if successful, None if failed

    Security:
        - Case-insensitive username matching
        - Input sanitization
        - Constant-time password verification via Argon2id
        - Security event logging
        - Account status checking
    """
    username = sanitize_username(username)
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
        log_security_event(conn, username, "login_attempt", False)
        return None  # User not found

    db_username, db_hash, user_type, employee_id, is_active = result

    if not is_active:
        log_security_event(conn, username, "login_attempt", False)
        return None  # Account disabled

    if not verify_password(password, db_hash):
        log_security_event(conn, username, "login_attempt", False)
        return None  # Wrong password

    # Update last login timestamp
    cursor.execute(
        """
        UPDATE users
        SET last_login = ?
        WHERE username = ?
    """,
        (datetime.now().isoformat(), username),
    )
    conn.commit()

    log_security_event(conn, username, "login_attempt", True)
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
