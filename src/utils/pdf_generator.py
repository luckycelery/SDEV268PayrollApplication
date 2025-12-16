"""
PDF Generation Utilities for Payroll Reports

Generates downloadable PDF reports for:
- Individual employee paychecks
- Payroll period summaries (all employees)
"""

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from src.models.employee import Employee
from src.models.payroll import PayrollDetail

# Reusable styles
styles = getSampleStyleSheet()
TITLE_STYLE = ParagraphStyle(
    "CustomTitle", parent=styles["Heading1"], fontSize=18, textColor=colors.HexColor("#1a1a1a"), spaceAfter=6
)
HEADER_STYLE = ParagraphStyle(
    "CustomHeader", parent=styles["Heading2"], fontSize=14, textColor=colors.HexColor("#333333"), spaceAfter=12
)


def format_currency(amount: float) -> str:
    """Format amount as currency."""
    return f"${amount:,.2f}"


def get_employee_name(employee_id: str) -> str:
    """Get formatted employee name or ID if not found."""
    employee = Employee.get_by_id(employee_id)
    return f"{employee.first_name} {employee.last_name}" if employee else employee_id


def generate_paycheck_pdf(detail: PayrollDetail, period_start: str, period_end: str) -> BytesIO:
    """
    Generate individual employee paycheck PDF.

    Args:
        detail: PayrollDetail object with employee's pay information
        period_start: Pay period start date (YYYY-MM-DD)
        period_end: Pay period end date (YYYY-MM-DD)

    Returns:
        BytesIO buffer containing PDF data
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5 * inch, bottomMargin=0.5 * inch)
    story = []

    # Get employee info
    employee = Employee.get_by_id(detail.employee_id)
    employee_name = get_employee_name(detail.employee_id)

    # Company header
    story.append(Paragraph("ABC Company", TITLE_STYLE))
    story.append(Paragraph("Payroll Statement", styles["Normal"]))
    story.append(Spacer(1, 0.2 * inch))

    # Employee and period info
    info_data = [
        ["Employee ID:", detail.employee_id, "Pay Period:", f"{period_start} to {period_end}"],
        ["Employee Name:", employee_name, "Pay Date:", period_end],
        ["Pay Type:", employee.salary_type if employee else "N/A", "", ""],
    ]
    info_table = Table(info_data, colWidths=[1.2 * inch, 2.3 * inch, 1.2 * inch, 2.3 * inch])
    info_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(info_table)
    story.append(Spacer(1, 0.3 * inch))

    # Earnings section
    story.append(Paragraph("Earnings", HEADER_STYLE))
    earnings_data = [
        ["Description", "Hours", "Rate/Amount", "Total"],
        [
            "Base Pay",
            f"{detail.regular_hours:.1f}",
            format_currency(detail.base_pay / detail.regular_hours if detail.regular_hours > 0 else 0),
            format_currency(detail.base_pay),
        ],
    ]

    if detail.overtime_hours > 0:
        earnings_data.append(
            [
                "Overtime Pay (1.5x)",
                f"{detail.overtime_hours:.1f}",
                "",
                format_currency(detail.overtime_pay),
            ]
        )

    if detail.saturday_hours > 0:
        earnings_data.append(
            [
                "Saturday Pay (1.5x)",
                f"{detail.saturday_hours:.1f}",
                "",
                format_currency(detail.saturday_pay),
            ]
        )

    if detail.pto_hours > 0:
        earnings_data.append(["PTO Hours", f"{detail.pto_hours:.1f}", "", ""])

    if detail.dependent_stipend > 0:
        earnings_data.append(["Dependent Stipend", "", "", format_currency(detail.dependent_stipend)])

    earnings_data.append(["", "", "Gross Pay:", format_currency(detail.gross_pay)])

    earnings_table = Table(earnings_data, colWidths=[2.5 * inch, 1.2 * inch, 1.5 * inch, 1.8 * inch])
    earnings_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e0e0e0")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                ("GRID", (0, 0), (-1, -2), 0.5, colors.grey),
                ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#f5f5f5")),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("LINEABOVE", (0, -1), (-1, -1), 1, colors.black),
            ]
        )
    )
    story.append(earnings_table)
    story.append(Spacer(1, 0.3 * inch))

    # Deductions section
    story.append(Paragraph("Deductions", HEADER_STYLE))
    deductions_data = [
        ["Description", "Amount"],
        ["Medical Insurance", format_currency(detail.medical_deduction)],
        ["Federal Tax", format_currency(detail.federal_tax_employee)],
        ["State Tax", format_currency(detail.state_tax)],
        ["Social Security", format_currency(detail.social_security_employee)],
        ["Medicare", format_currency(detail.medicare_employee)],
        ["Total Deductions:", format_currency(detail.total_employee_taxes)],
    ]

    deductions_table = Table(deductions_data, colWidths=[5.2 * inch, 1.8 * inch])
    deductions_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e0e0e0")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                ("GRID", (0, 0), (-1, -2), 0.5, colors.grey),
                ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#f5f5f5")),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("LINEABOVE", (0, -1), (-1, -1), 1, colors.black),
            ]
        )
    )
    story.append(deductions_table)
    story.append(Spacer(1, 0.3 * inch))

    # Employer Taxes (Informational)
    story.append(Paragraph("Employer Taxes (Informational)", HEADER_STYLE))
    story.append(
        Paragraph(
            "<i>These amounts are paid by your employer and do not affect your paycheck.</i>",
            styles["Italic"],
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    employer_taxes_data = [
        ["Description", "Amount"],
        ["Federal Tax", format_currency(detail.federal_tax_employer)],
        ["Social Security", format_currency(detail.social_security_employer)],
        ["Medicare", format_currency(detail.medicare_employer)],
        ["Total Employer Taxes:", format_currency(detail.total_employer_taxes)],
    ]

    employer_taxes_table = Table(employer_taxes_data, colWidths=[5.2 * inch, 1.8 * inch])
    employer_taxes_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17a2b8")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                ("GRID", (0, 0), (-1, -2), 0.5, colors.grey),
                ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#d1ecf1")),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("LINEABOVE", (0, -1), (-1, -1), 1, colors.black),
            ]
        )
    )
    story.append(employer_taxes_table)
    story.append(Spacer(1, 0.3 * inch))

    # Net Pay (highlighted)
    net_pay_data = [["NET PAY:", format_currency(detail.net_pay)]]
    net_pay_table = Table(net_pay_data, colWidths=[5.2 * inch, 1.8 * inch])
    net_pay_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#4CAF50")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 14),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    story.append(net_pay_table)

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_payroll_summary_pdf(details: list[PayrollDetail], period_start: str, period_end: str) -> BytesIO:
    """
    Generate payroll summary PDF for all employees in a period.

    Args:
        details: List of PayrollDetail objects
        period_start: Pay period start date (YYYY-MM-DD)
        period_end: Pay period end date (YYYY-MM-DD)

    Returns:
        BytesIO buffer containing PDF data
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter, topMargin=0.5 * inch, bottomMargin=0.5 * inch, leftMargin=0.5 * inch
    )
    story = []

    # Company header
    story.append(Paragraph("ABC Company", TITLE_STYLE))
    story.append(Paragraph("Payroll Summary Report", styles["Normal"]))
    story.append(Paragraph(f"Pay Period: {period_start} to {period_end}", styles["Normal"]))
    story.append(Spacer(1, 0.3 * inch))

    # Summary table
    table_data = [["ID", "Employee Name", "Type", "Hours", "Gross Pay", "Deductions", "Net Pay"]]

    total_gross = 0.0
    total_deductions = 0.0
    total_net = 0.0

    for detail in sorted(details, key=lambda d: d.employee_id):
        employee = Employee.get_by_id(detail.employee_id)
        employee_name = get_employee_name(detail.employee_id)
        salary_type = (employee.salary_type or "N/A") if employee else "N/A"
        total_hours = detail.regular_hours + detail.overtime_hours + detail.saturday_hours

        table_data.append(
            [
                detail.employee_id,
                employee_name,
                salary_type,
                f"{total_hours:.1f}",
                format_currency(detail.gross_pay),
                format_currency(detail.total_employee_taxes),
                format_currency(detail.net_pay),
            ]
        )

        total_gross += detail.gross_pay
        total_deductions += detail.total_employee_taxes
        total_net += detail.net_pay

    # Totals row
    table_data.append(
        [
            "",
            "TOTALS",
            "",
            "",
            format_currency(total_gross),
            format_currency(total_deductions),
            format_currency(total_net),
        ]
    )

    # Create table
    summary_table = Table(table_data, colWidths=[0.6 * inch, 1.8 * inch, 0.7 * inch, 0.6 * inch, 1.1 * inch, 1.1 * inch, 1.1 * inch])
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("BACKGROUND", (0, 1), (-1, -2), colors.white),
                ("GRID", (0, 0), (-1, -2), 0.5, colors.grey),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("ALIGN", (3, 1), (-1, -1), "RIGHT"),
                # Totals row styling
                ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#e0e0e0")),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("LINEABOVE", (0, -1), (-1, -1), 2, colors.black),
                ("FONTSIZE", (0, -1), (-1, -1), 9),
            ]
        )
    )
    story.append(summary_table)

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
