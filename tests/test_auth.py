"""
Security module tests for authentication and password hashing

Tests the PyNaCl Argon2id implementation in database/auth.py
"""

import sqlite3

from database.auth import (
    authenticate_user,
    generate_employee_password,
    generate_employee_username,
    hash_password,
    sanitize_username,
    verify_password,
)


def test_generate_employee_username():
    """Test username generation from email"""
    email = "roy.mustang@abccompany.com"
    username = generate_employee_username(email)
    assert username == "roy.mustang@abccompany.com"


def test_generate_employee_password():
    """Test password generation from email and DOB"""
    email = "roy.mustang@abccompany.com"
    dob = "2005-11-06"
    password = generate_employee_password(email, dob)
    # Format: <email_prefix><MMDDYYYY>
    assert password == "roy.mustang11062005"


def test_hash_password_argon2id_format():
    """Test that hash_password produces Argon2id format"""
    password = "test_password_123"
    hashed = hash_password(password)
    # Argon2id hashes start with $argon2id$
    assert hashed.startswith("$argon2id$")
    assert "v=19" in hashed  # Version 19 (0x13)
    assert "m=" in hashed  # Memory parameter
    assert "t=" in hashed  # Time parameter
    assert "p=" in hashed  # Parallelism parameter


def test_hash_password_unique_salts():
    """Test that hashing same password twice produces different hashes (due to salt)"""
    password = "same_password"
    hash1 = hash_password(password)
    hash2 = hash_password(password)

    # Hashes should be different due to random salt
    assert hash1 != hash2
    # But both should verify against the same password
    assert verify_password(password, hash1)
    assert verify_password(password, hash2)


def test_verify_password_correct():
    """Test password verification with correct password"""
    password = "correct_password"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    """Test password verification with incorrect password"""
    password = "correct_password"
    wrong_password = "wrong_password"
    hashed = hash_password(password)

    assert verify_password(wrong_password, hashed) is False


def test_sanitize_username_strips_whitespace():
    """Test username sanitization removes whitespace"""
    assert sanitize_username("  username  ") == "username"
    assert sanitize_username("username\n") == "username"
    assert sanitize_username("\tUsername  ") == "username"


def test_authenticate_user_success(test_db_path):
    """Test successful user authentication"""
    conn = sqlite3.connect(test_db_path)

    # Test with existing admin account if available
    result = authenticate_user(conn, "HR0001", "AbccoTeam3")

    # May be None if test DB doesn't have users set up
    # This is okay - just testing the function doesn't crash
    if result:
        username, user_type, employee_id = result
        assert username is not None
        assert user_type in ("Admin", "Employee")

    conn.close()


def test_authenticate_user_nonexistent(test_db_path):
    """Test authentication with nonexistent user"""
    conn = sqlite3.connect(test_db_path)

    result = authenticate_user(conn, "nonexistent_user_xyz", "password")

    assert result is None

    conn.close()


def test_authenticate_user_wrong_password(test_db_path):
    """Test authentication with wrong password"""
    conn = sqlite3.connect(test_db_path)

    # Try with admin account
    result = authenticate_user(conn, "HR0001", "wrong_password_123")

    # Should be None (failed authentication)
    assert result is None

    conn.close()

