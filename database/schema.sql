-- =============================================================================
-- ABC Company Payroll System - Database Schema
-- Python + SQLite3 + tkinter
-- Schema Lock Version
-- =============================================================================

-- Drop existing tables if recreating database
DROP TABLE IF EXISTS payroll_details;
DROP TABLE IF EXISTS time_entries;
DROP TABLE IF EXISTS payroll_periods;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS compensation;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS job_titles;
DROP TABLE IF EXISTS departments;

-- =============================================================================
-- REFERENCE TABLES
-- =============================================================================

CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT NOT NULL UNIQUE,
    created_date TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE job_titles (
    job_title_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title_name TEXT NOT NULL UNIQUE,
    created_date TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- =============================================================================
-- EMPLOYEE CORE DATA
-- =============================================================================

CREATE TABLE employees (
    employee_id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    surname TEXT,
    date_of_birth TEXT NOT NULL,
    gender TEXT NOT NULL CHECK(gender IN ('Male', 'Female')),
    email TEXT NOT NULL UNIQUE,
    phone_num TEXT,
    address_line1 TEXT NOT NULL,
    address_line2 TEXT,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip_code TEXT NOT NULL,
    has_picture INTEGER NOT NULL DEFAULT 0,
    picture_filename TEXT,
    status TEXT NOT NULL DEFAULT 'Active' CHECK(status IN ('Active', 'Terminated')),
    date_hired TEXT NOT NULL,
    department_name TEXT NOT NULL,
    job_title_name TEXT NOT NULL,
    created_date TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    modified_date TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (department_name) REFERENCES departments(department_name),
    FOREIGN KEY (job_title_name) REFERENCES job_titles(title_name)
);

-- =============================================================================
-- COMPENSATION DATA
-- =============================================================================

CREATE TABLE compensation (
    compensation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT NOT NULL UNIQUE,
    salary_type TEXT NOT NULL CHECK(salary_type IN ('Salary', 'Hourly')),
    base_salary REAL,
    hourly_rate REAL,
    medical_type TEXT NOT NULL CHECK(medical_type IN ('Single', 'Family')),
    num_dependents INTEGER NOT NULL DEFAULT 0 CHECK(num_dependents >= 0),
    effective_date TEXT NOT NULL,
    created_date TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    modified_date TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    CHECK (
        (salary_type = 'Salary' AND base_salary IS NOT NULL AND base_salary > 0 AND hourly_rate IS NULL) OR
        (salary_type = 'Hourly' AND hourly_rate IS NOT NULL AND hourly_rate > 0 AND base_salary IS NULL)
    )
);

-- =============================================================================
-- AUTHENTICATION & USER ACCOUNTS
-- =============================================================================

-- HR0001 for admin, email prefix for employees
-- SHA256 hash (upgrade to bcrypt later)
-- employee_id NULL for Admin users
-- is_active for soft delete
-- last_login is ISO timestamp of last login
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    user_type TEXT NOT NULL CHECK(user_type IN ('Admin', 'Employee')),
    employee_id TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    last_login TEXT,
    created_date TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

-- =============================================================================
-- PAYROLL PERIODS
-- =============================================================================

-- ISO format: YYYY-MM-DD (Monday) for period_start_date
-- ISO format: YYYY-MM-DD (Sunday) for period_end_date
-- processed_date: NULL until payroll is calculated
-- is_locked: 1 = locked, no more edits allowed
-- processed_by: Admin username who processed
CREATE TABLE payroll_periods (
    payroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
    period_start_date TEXT NOT NULL,
    period_end_date TEXT NOT NULL,
    processed_date TEXT,
    is_locked INTEGER NOT NULL DEFAULT 0,
    processed_by TEXT,
    created_date TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    UNIQUE(period_start_date, period_end_date),
    CHECK (date(period_end_date) >= date(period_start_date))
);

-- =============================================================================
-- TIME ENTRIES (Daily records for each employee)
-- =============================================================================

-- payroll_id: NULL until assigned to a payroll period
-- entry_date: ISO format YYYY-MM-DD
-- is_saturday: Boolean, 1 for Saturday (time and a half)
-- notes: Optional notes for admin adjustments
-- UNIQUE constraint: One entry per employee per day
CREATE TABLE time_entries (
    time_entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT NOT NULL,
    payroll_id INTEGER,
    entry_date TEXT NOT NULL,
    day_of_week TEXT NOT NULL CHECK(day_of_week IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')),
    hours_worked REAL NOT NULL DEFAULT 0,
    pto_hours REAL NOT NULL DEFAULT 0,
    is_saturday INTEGER NOT NULL DEFAULT 0,
    notes TEXT,
    created_date TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    modified_date TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (payroll_id) REFERENCES payroll_periods(payroll_id),
    UNIQUE(employee_id, entry_date),
    CHECK (hours_worked >= 0 AND hours_worked <= 24),
    CHECK (pto_hours >= 0 AND pto_hours <= 8),
    CHECK (pto_hours + hours_worked <= 24)
);

-- =============================================================================
-- PTO BALANCES (Track accumulated PTO)
-- =============================================================================

-- total_accrued: Total PTO earned
-- total_used: Total PTO used
-- balance: Current balance (accrued - used)
-- CHECK constraints: Balance can't go negative, max 80 hours PTO balance
CREATE TABLE pto_balances (
    pto_balance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT NOT NULL UNIQUE,
    total_accrued REAL NOT NULL DEFAULT 0,
    total_used REAL NOT NULL DEFAULT 0,
    balance REAL NOT NULL DEFAULT 0,
    last_updated TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    CHECK (balance >= 0),
    CHECK (balance <= 80)
);

-- =============================================================================
-- PAYROLL CALCULATION RESULTS
-- =============================================================================

-- Hours breakdown:
--   overtime_hours: Hours over 8/day
--   saturday_hours: Saturday hours (all at 1.5x)
-- Gross pay calculation:
--   base_pay: Regular hours * rate
--   overtime_pay: OT hours * 1.5 * rate
--   saturday_pay: Saturday hours * 1.5 * rate
--   gross_pay: Sum of all pay components
-- Pre-tax deductions (applied to gross):
--   medical_deduction: $50 single, $100 family
--   dependent_stipend: $45 per dependent (negative deduction)
-- Taxable income (after pre-tax adjustments):
--   taxable_income: gross - medical + stipend
-- Tax calculations (applied to taxable income):
--   state_tax: IN 3.15%
--   federal_tax_employee: 7.65%
--   social_security_employee: 6.2%
--   medicare_employee: 1.45%
-- Net pay (what employee receives):
--   net_pay: taxable_income - total_employee_taxes
-- Employer taxes (for reporting, not deducted from employee):
--   federal_tax_employer: 7.65%
--   social_security_employer: 6.2%
--   medicare_employer: 1.45%
-- UNIQUE constraint: One detail record per employee per payroll
CREATE TABLE payroll_details (
    payroll_detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
    payroll_id INTEGER NOT NULL,
    employee_id TEXT NOT NULL,

    regular_hours REAL NOT NULL DEFAULT 0,
    overtime_hours REAL NOT NULL DEFAULT 0,
    saturday_hours REAL NOT NULL DEFAULT 0,
    pto_hours REAL NOT NULL DEFAULT 0,
    total_hours REAL NOT NULL DEFAULT 0,

    base_pay REAL NOT NULL DEFAULT 0,
    overtime_pay REAL NOT NULL DEFAULT 0,
    saturday_pay REAL NOT NULL DEFAULT 0,
    gross_pay REAL NOT NULL DEFAULT 0,

    medical_deduction REAL NOT NULL DEFAULT 0,
    dependent_stipend REAL NOT NULL DEFAULT 0,

    taxable_income REAL NOT NULL DEFAULT 0,

    state_tax REAL NOT NULL DEFAULT 0,
    federal_tax_employee REAL NOT NULL DEFAULT 0,
    social_security_employee REAL NOT NULL DEFAULT 0,
    medicare_employee REAL NOT NULL DEFAULT 0,
    total_employee_taxes REAL NOT NULL DEFAULT 0,

    net_pay REAL NOT NULL DEFAULT 0,

    federal_tax_employer REAL NOT NULL DEFAULT 0,
    social_security_employer REAL NOT NULL DEFAULT 0,
    medicare_employer REAL NOT NULL DEFAULT 0,
    total_employer_taxes REAL NOT NULL DEFAULT 0,

    calculated_date TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),

    FOREIGN KEY (payroll_id) REFERENCES payroll_periods(payroll_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    UNIQUE(payroll_id, employee_id)
);

-- =============================================================================
-- INDEXES FOR PERFORMANCE
-- =============================================================================

-- Employee lookups
CREATE INDEX idx_employees_status ON employees(status);
CREATE INDEX idx_employees_department ON employees(department_name);
CREATE INDEX idx_employees_email ON employees(email);
CREATE INDEX idx_employees_last_name ON employees(last_name);

-- Time entry queries
CREATE INDEX idx_time_entries_employee ON time_entries(employee_id);
CREATE INDEX idx_time_entries_payroll ON time_entries(payroll_id);
CREATE INDEX idx_time_entries_date ON time_entries(entry_date);
CREATE INDEX idx_time_entries_employee_date ON time_entries(employee_id, entry_date);

-- Payroll queries
CREATE INDEX idx_payroll_details_payroll ON payroll_details(payroll_id);
CREATE INDEX idx_payroll_details_employee ON payroll_details(employee_id);
CREATE INDEX idx_payroll_periods_dates ON payroll_periods(period_start_date, period_end_date);

-- User authentication
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_employee ON users(employee_id);

-- =============================================================================
-- VIEWS FOR COMMON QUERIES
-- =============================================================================

-- View: Employee full information (demographics + compensation + PTO)
CREATE VIEW vw_employee_full AS
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    e.surname,
    e.date_of_birth,
    e.gender,
    e.email,
    e.phone_num,
    e.address_line1,
    e.address_line2,
    e.city,
    e.state,
    e.zip_code,
    e.has_picture,
    e.picture_filename,
    e.status,
    e.date_hired,
    d.department_name,
    j.title_name AS job_title_name,
    c.salary_type,
    c.base_salary,
    c.hourly_rate,
    c.medical_type,
    c.num_dependents,
    COALESCE(p.total_accrued, 0) AS pto_accrued,
    COALESCE(p.total_used, 0) AS pto_used,
    COALESCE(p.balance, 0) AS pto_balance
FROM employees e
JOIN departments d ON e.department_name = d.department_name
JOIN job_titles j ON e.job_title_name = j.title_name
LEFT JOIN compensation c ON e.employee_id = c.employee_id
LEFT JOIN pto_balances p ON e.employee_id = p.employee_id;

-- View: Weekly time entry summary per employee
CREATE VIEW vw_weekly_time_summary AS
SELECT
    te.employee_id,
    te.payroll_id,
    strftime('%Y-%W', te.entry_date) AS year_week,
    SUM(te.hours_worked) AS total_hours_worked,
    SUM(te.pto_hours) AS total_pto_hours,
    SUM(CASE WHEN te.is_saturday = 1 THEN te.hours_worked ELSE 0 END) AS saturday_hours,
    SUM(CASE WHEN te.hours_worked > 8 THEN te.hours_worked - 8 ELSE 0 END) AS overtime_hours
FROM time_entries te
GROUP BY te.employee_id, te.payroll_id, year_week;

-- =============================================================================
-- TRIGGERS FOR DATA INTEGRITY
-- =============================================================================

-- Trigger: Update modified_date on employee record changes
CREATE TRIGGER trg_employees_update_modified
AFTER UPDATE ON employees
FOR EACH ROW
BEGIN
    UPDATE employees
    SET modified_date = datetime('now', 'localtime')
    WHERE employee_id = NEW.employee_id;
END;

-- Trigger: Update modified_date on compensation changes
CREATE TRIGGER trg_compensation_update_modified
AFTER UPDATE ON compensation
FOR EACH ROW
BEGIN
    UPDATE compensation
    SET modified_date = datetime('now', 'localtime')
    WHERE compensation_id = NEW.compensation_id;
END;

-- Trigger: Update modified_date on time entry changes
CREATE TRIGGER trg_time_entries_update_modified
AFTER UPDATE ON time_entries
FOR EACH ROW
BEGIN
    UPDATE time_entries
    SET modified_date = datetime('now', 'localtime')
    WHERE time_entry_id = NEW.time_entry_id;
END;

-- Trigger: Update PTO balance when PTO is used
CREATE TRIGGER trg_time_entries_update_pto_balance
AFTER INSERT ON time_entries
FOR EACH ROW
WHEN NEW.pto_hours > 0
BEGIN
    -- Ensure employee has PTO balance record
    INSERT OR IGNORE INTO pto_balances (employee_id, total_accrued, total_used, balance)
    VALUES (NEW.employee_id, 0, 0, 0);

    -- Update PTO usage
    UPDATE pto_balances
    SET total_used = total_used + NEW.pto_hours,
        balance = balance - NEW.pto_hours,
        last_updated = datetime('now', 'localtime')
    WHERE employee_id = NEW.employee_id;
END;

-- Trigger: Prevent time entry edits after payroll is locked
CREATE TRIGGER trg_prevent_locked_payroll_edits
BEFORE UPDATE ON time_entries
FOR EACH ROW
WHEN NEW.payroll_id IS NOT NULL
BEGIN
    SELECT CASE
        WHEN (SELECT is_locked FROM payroll_periods WHERE payroll_id = NEW.payroll_id) = 1
        THEN RAISE(ABORT, 'Cannot edit time entries for locked payroll period')
    END;
END;


-- =============================================================================
-- END OF SCHEMA
-- =============================================================================
