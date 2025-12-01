"""
Authentication Routes - Login/Logout functionality
"""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from database.auth import authenticate_user
from src.models.base_model import BaseModel

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")

        # Basic validation
        if not username or not password:
            flash("Please enter both username and password.", "error")
            return render_template("auth/login.html")

        # Authenticate against database
        conn = BaseModel.get_connection()
        try:
            result = authenticate_user(conn, username, password)

            if result is None:
                flash("Invalid username or password.", "error")
                return render_template("auth/login.html")

            auth_username, user_type, employee_id = result

            # Set session data
            session["user_id"] = employee_id if employee_id else auth_username
            session["username"] = auth_username
            session["user_type"] = user_type
            session["employee_id"] = employee_id

            if user_type == "Admin":
                flash("Welcome, Admin!", "success")
                return redirect(url_for("admin.dashboard"))
            else:
                flash("Welcome!", "success")
                return redirect(url_for("employee.dashboard"))
        finally:
            conn.close()

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Handle user logout."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
