"""
Calculate Payroll for a Week

This script calculates payroll for all employees for a specified week.

Usage:
    uv run python src/utils/calculate_payroll.py [start_date] [end_date]

    If no dates are specified, defaults to first week (Nov 3-9, 2025)

Example:
    uv run python src/utils/calculate_payroll.py 2025-11-03 2025-11-09
"""

import sys

# Add project root to path for imports
from constants import PROJECT_ROOT

sys.path.insert(0, str(PROJECT_ROOT))

from src.controllers.payroll_controller import PayrollController
from src.models.employee import Employee
from src.models.payroll import PayrollDetail


def format_currency(amount: float) -> str:
    """Format amount as currency."""
    return f"${amount:,.2f}"


def get_employee_info(employee_id: str) -> tuple[str, str]:
    """Get employee name and salary type."""
    employee = Employee.get_by_id(employee_id)
    if employee:
        name = f"{employee.first_name} {employee.last_name}"
        salary_type = employee.salary_type or "Unknown"
        return name, salary_type
    return employee_id, "Unknown"


def print_payroll_summary(details: list[PayrollDetail]) -> None:
    """Print a formatted summary of payroll calculations."""
    print("\n" + "=" * 105)
    print(f"{'Employee':<10} {'Name':<20} {'Type':<8} {'Hours':>8} {'OT Hrs':>8} {'Gross':>12} {'Taxes':>12} {'Net':>12}")
    print("=" * 105)

    total_gross = 0.0
    total_taxes = 0.0
    total_net = 0.0

    for detail in sorted(details, key=lambda d: d.employee_id):
        name, salary_type = get_employee_info(detail.employee_id)
        total_hours = detail.regular_hours + detail.overtime_hours + detail.saturday_hours
        total_taxes_emp = detail.total_employee_taxes

        print(
            f"{detail.employee_id:<10} "
            f"{name:<20} "
            f"{salary_type:<8} "
            f"{total_hours:>8.1f} "
            f"{detail.overtime_hours:>8.1f} "
            f"{format_currency(detail.gross_pay):>12} "
            f"{format_currency(total_taxes_emp):>12} "
            f"{format_currency(detail.net_pay):>12}"
        )

        total_gross += detail.gross_pay
        total_taxes += total_taxes_emp
        total_net += detail.net_pay

    print("=" * 105)
    print(
        f"{'TOTALS':<10} {'':<20} {'':<8} {'':<8} {'':<8} "
        f"{format_currency(total_gross):>12} "
        f"{format_currency(total_taxes):>12} "
        f"{format_currency(total_net):>12}"
    )


def print_detailed_breakdown(detail: PayrollDetail) -> None:
    """Print detailed breakdown for one employee."""
    name, salary_type = get_employee_info(detail.employee_id)
    print(f"\n--- {detail.employee_id}: {name} ({salary_type}) ---")
    print(f"  Regular Hours:    {detail.regular_hours:>8.1f}  |  Base Pay:        {format_currency(detail.base_pay):>12}")
    print(f"  Overtime Hours:   {detail.overtime_hours:>8.1f}  |  Overtime Pay:    {format_currency(detail.overtime_pay):>12}")
    print(f"  Saturday Hours:   {detail.saturday_hours:>8.1f}  |  Saturday Pay:    {format_currency(detail.saturday_pay):>12}")
    print(f"  PTO Hours:        {detail.pto_hours:>8.1f}  |  Dependent Stipend:{format_currency(detail.dependent_stipend):>11}")
    print(f"                              |  GROSS PAY:       {format_currency(detail.gross_pay):>12}")
    print("  Deductions:")
    print(f"    Medical:        {format_currency(detail.medical_deduction):>12}")
    print(f"    Federal Tax:    {format_currency(detail.federal_tax_employee):>12}")
    print(f"    State Tax:      {format_currency(detail.state_tax):>12}")
    print(f"    Social Security:{format_currency(detail.social_security_employee):>12}")
    print(f"    Medicare:       {format_currency(detail.medicare_employee):>12}")
    print(f"                              |  NET PAY:         {format_currency(detail.net_pay):>12}")


def main():
    """Main entry point."""
    # Parse dates
    if len(sys.argv) >= 3:
        start_date = sys.argv[1]
        end_date = sys.argv[2]
    else:
        # Default to first week of November 2025
        start_date = "2025-11-10"
        end_date = "2025-11-16"

    print("=" * 60)
    print("Payroll Calculation")
    print("=" * 60)
    print(f"Period: {start_date} to {end_date}")

    # Initialize controller
    controller = PayrollController()

    # Calculate payroll for all employees
    print("\nCalculating payroll for all employees...")
    success, message, results = controller.calculate_all_payroll(start_date, end_date)

    print(f"\n{message}")

    if results:
        print_payroll_summary(results)

        # Show detailed breakdown option
        print("\n\nDetailed Breakdown:")
        for detail in sorted(results, key=lambda d: d.employee_id):
            print_detailed_breakdown(detail)

    print("\nDone!")


if __name__ == "__main__":
    main()
