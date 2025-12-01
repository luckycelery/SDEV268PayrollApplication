"""
Application Constants

Centralized configuration values used across the payroll system.
"""

# =============================================================================
# APPLICATION METADATA
# =============================================================================

APP_NAME = "ABC Company Payroll System"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Automated payroll management for ABC Company"
APP_AUTHOR = "Group 3"
APP_COURSE = "SDEV268, Winter 2025"


# =============================================================================
# PAY PERIOD CONFIGURATION
# =============================================================================

# Pay period cycle (weekly)
PAY_PERIOD_DAYS = 7
WEEKS_PER_YEAR = 52

# Day of week (Python's weekday(): Monday=0, Sunday=6)
PAY_PERIOD_START_DAY = 0  # Monday
PAY_PERIOD_END_DAY = 6    # Sunday

# Day names for display/validation
PAY_PERIOD_START_DAY_NAME = "Monday"
PAY_PERIOD_END_DAY_NAME = "Sunday"


# =============================================================================
# EMPLOYEE CONFIGURATION
# =============================================================================

# Minimum age requirement
MIN_EMPLOYEE_AGE = 18

# Employee ID format
EMPLOYEE_ID_PREFIX = "E"
EMPLOYEE_ID_LENGTH = 4  # Total length including prefix (E001)

# Status values
EMPLOYEE_STATUS_ACTIVE = "Active"
EMPLOYEE_STATUS_TERMINATED = "Terminated"

# Gender values
GENDER_MALE = "Male"
GENDER_FEMALE = "Female"
VALID_GENDERS = [GENDER_MALE, GENDER_FEMALE]


# =============================================================================
# COMPENSATION CONFIGURATION
# =============================================================================

# Salary types
SALARY_TYPE_SALARY = "Salary"
SALARY_TYPE_HOURLY = "Hourly"
VALID_SALARY_TYPES = [SALARY_TYPE_SALARY, SALARY_TYPE_HOURLY]

# Medical plan types
MEDICAL_TYPE_SINGLE = "Single"
MEDICAL_TYPE_FAMILY = "Family"
VALID_MEDICAL_TYPES = [MEDICAL_TYPE_SINGLE, MEDICAL_TYPE_FAMILY]


# =============================================================================
# TIME ENTRY CONFIGURATION
# =============================================================================

# Work hours
STANDARD_WORK_HOURS_PER_DAY = 8
STANDARD_WORK_HOURS_PER_WEEK = 40
MAX_HOURS_PER_DAY = 24
OVERTIME_THRESHOLD_DAILY = 8  # Hours over this are overtime

# PTO limits
MAX_PTO_HOURS_PER_DAY = 8
MAX_PTO_BALANCE = 80  # Maximum PTO hours that can be banked

# Salaried employee automatic hours (Mon-Fri)
SALARIED_AUTO_HOURS_PER_DAY = 8
SALARIED_WORK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


# =============================================================================
# VALIDATION PATTERNS
# =============================================================================

# Email must contain @ symbol (basic check)
EMAIL_PATTERN = r"^[^@]+@[^@]+\.[^@]+$"

# State abbreviation (2 uppercase letters)
STATE_PATTERN = r"^[A-Z]{2}$"

# ZIP code (5 digits or 5+4 format)
ZIP_CODE_PATTERN = r"^\d{5}(-\d{4})?$"


# =============================================================================
# VALIDATION THRESHOLDS (for anomaly detection)
# =============================================================================

# Flag unusual hour entries (per project requirements)
MAX_REASONABLE_WEEKLY_HOURS = 80  # Flag entries over this as unusual
MIN_REASONABLE_WEEKLY_HOURS = 0


# =============================================================================
# USER / AUTHENTICATION
# =============================================================================

USER_TYPE_ADMIN = "Admin"
USER_TYPE_EMPLOYEE = "Employee"
VALID_USER_TYPES = [USER_TYPE_ADMIN, USER_TYPE_EMPLOYEE]

# Admin default credentials
ADMIN_DEFAULT_USER_ID = "HR0001"

# Employee credential generation: based on email prefix + DOB
# (actual password logic handled in auth module)


# =============================================================================
# DAYS OF WEEK
# =============================================================================

DAYS_OF_WEEK = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


# =============================================================================
# PAYROLL CALCULATION RATES
# =============================================================================

# Overtime multiplier (time and a half)
OVERTIME_MULTIPLIER = 1.5
SATURDAY_MULTIPLIER = 1.5  # All Saturday hours at 1.5x

# Medical deductions (per pay period)
MEDICAL_DEDUCTION_SINGLE = 50.00
MEDICAL_DEDUCTION_FAMILY = 100.00

# Dependent stipend (per dependent per pay period)
DEPENDENT_STIPEND_PER_DEPENDENT = 45.00

# Tax rates (as decimals)
STATE_TAX_RATE_IN = 0.0315           # Indiana 3.15%
FEDERAL_TAX_RATE_EMPLOYEE = 0.0765   # 7.65%
SOCIAL_SECURITY_RATE_EMPLOYEE = 0.062  # 6.2%
MEDICARE_RATE_EMPLOYEE = 0.0145      # 1.45%

# Employer tax rates (for reporting)
FEDERAL_TAX_RATE_EMPLOYER = 0.0765   # 7.65%
SOCIAL_SECURITY_RATE_EMPLOYER = 0.062  # 6.2%
MEDICARE_RATE_EMPLOYER = 0.0145      # 1.45%
