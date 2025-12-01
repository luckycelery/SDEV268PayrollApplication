"""
Routes Package - Flask Blueprints

Contains route blueprints for different parts of the application:
- auth: Login/logout
- admin: Admin-only functionality
- employee: Employee self-service
- payroll: Payroll management
"""

from src.routes import admin, auth, employee, payroll

__all__ = ["auth", "admin", "employee", "payroll"]
