"""
ABC Payroll System - Flask Application Factory

This module creates and configures the Flask application.
"""

import os

from flask import Flask


def create_app(config=None):
    """
    Flask application factory.

    Args:
        config: Optional configuration dictionary

    Returns:
        Configured Flask application instance
    """
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    # Default configuration
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production"),
        DATABASE=os.path.join(os.path.dirname(os.path.dirname(__file__)), "payroll.db"),
    )

    # Override with provided config
    if config:
        app.config.update(config)

    # Initialize database path for models
    from src.models.base_model import BaseModel
    BaseModel.set_db_path(app.config["DATABASE"])

    # Register blueprints
    from src.routes import admin, auth, employee, payroll, admin_time_entry

    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp, url_prefix="/admin")
    app.register_blueprint(employee.bp, url_prefix="/employee")
    app.register_blueprint(payroll.bp, url_prefix="/payroll")
    app.register_blueprint(admin_time_entry.bp, url_prefix="/admin/time-entry")

    # Add a simple index route that redirects to login
    @app.route("/")
    def index():
        from flask import redirect, url_for

        return redirect(url_for("auth.login"))

    return app
