# Payroll Application Testing Log

## Initial Log

## Profile Creation Tests

| Test Case ID | Employee | Scenario | Input Data | Expected Result | Actual Result | Screenshot (testing\screenshots\Testing Log Screenshots) | Status |
|--------------|----------|----------|------------|-----------------|---------------|----------------------------------------------------------|--------|
| TC001a       | Roy Mustang | Add Employee Profile | Full profile data entered | Profile saved successfully | Profile saved successfully | TC001a.png | Pass |
| TC002a       | Alfonse Elrich | Add Employee Profile | Full profile data entered | Profile saved successfully | Profile saved successfully | TC002a.png | Pass |
| TC003a       | Salim Bradley | Add Employee Profile | Full profile data entered - DOB under 18 | Error Message: Age under 18 | Error Message: Age under 18 | TC003a_006a_012a.png | Pass |
| TC004a       | Bruce Lee |  Add Employee Profile | Full profile data entered | Profile saved successfully | Profile saved successfully | TC004a.png | Pass |
| TC005a       | Edward Elrich Sr. |  Add Employee Profile | Full profile data entered | Profile saved successfully | Profile saved successfully | TC005a.png | Pass |
| TC006a       | Riza Hawkeye |  Add Employee Profile | Full profile data entered - no gender endtered| Error Message: Gender must be entered | Error Message: Gender must be entered | TC003a_006a_012a.png | Pass |
| TC007a       | Junji Ito Jr. | Add Employee Profile | Full profile data entered | Profile saved successfully | Profile saved successfully | TC007a.png | Pass |
| TC008a       | Sir Ken Kaneki | Add Employee Profile | Full profile data entered | Profile saved successfully | Profile saved successfully | TC008a.png | Pass |
| TC009a       | Toji Fushiguro | Add Employee Profile | Full profile data entered | Profile saved successfully | Profile saved successfully | TC009a.png | Pass |
| TC010a       | Ken Kuroko | Add Employee Profile | Full profile data entered | Profile saved successfully | Profile saved successfully | TC010a.png | Pass |
| TC011a       | Eto Yoshimura | Add Employee Profile | Full profile data entered | Profile saved successfully | Profile saved successfully | TC011a.png | Pass |
| TC012a       | Juuzou Suzuya | Add Employee Profile | Full profile data entered - start date after present| Error Message: Start Date must be before or at today's date| Error Message: Start Date must be before or at today's date | TC003a_006a_012a.png | Pass |

## Payroll Calculation Tests

## TC001 – Roy Mustang (Payroll Calculation)

| Field                          | Value |
|--------------------------------|-------|
| **Test Case ID**               | TC001b |
| **Employee**                   | Roy Mustang |
| **Salary Type**                | Salary |
| **Medical Type**               | Single |
| **Dependents**                 | 0 |
| **Base Salary (per week/hour)**| $3,000.00 |
| **Hours Worked**               | 40 |
| **Saturday Hours**             | 0 |
| **PTO Hours**                  | 0 |
| **Expected Gross Income**      | $3,000.00 |
| **Expected Medical Deduction** | $50.00 |
| **Expected Dependent Stipend** | $0.00 |
| **Expected Taxable Income (TI)** | $2,950.00 |
| **Expected State Tax (3.15%)** | $92.92 |
| **Expected Federal Tax (7.65%)** | $225.68 |
| **Expected Social Security (6.2%)** | $182.90 |
| **Expected Medicare (1.45%)**  | $42.77 | 
| **Expected Taxes Owed**        | $544.27 |
| **Expected Net Pay**           | $2,405.73 |
| **Actual Result**              | Values Display as Explected |
| **Screenshot**                 | TC001b.png |
| **Status**                     | Pass |

## TC002 – Alfonse Elrich (Payroll Calculation)

| Field                          | Value |
|--------------------------------|-------|
| **Test Case ID**               | TC002b |
| **Employee**                   | Alfonse Elrich |
| **Salary Type**                | Salary |
| **Medical Type**               | Single |
| **Dependents**                 | 0 |
| **Base Salary (per week/hour)**| $5,000.00 |
| **Hours Worked**               | 40 |
| **Saturday Hours**             | 0 |
| **PTO Hours**                  | 4 |
| **Expected Gross Income**      | $5000.00 |
| **Expected Medical Deduction** | $50.00 |
| **Expected Dependent Stipend** | $0.00 |
| **Expected Taxable Income (TI)** | $4,950.00 |
| **Expected State Tax (3.15%)** | $155.93 |
| **Expected Federal Tax (7.65%)** | $378.68 |
| **Expected Social Security (6.2%)** | $306.90 |
| **Expected Medicare (1.45%)**  | $71.78 |
| **Expected Taxes Owed**        | $913.27 |
| **Expected Net Pay**           | $4,036.73 |
| **Actual Result**              | Values Display as Explected |
| **Screenshot**                 | TC002b.png |
| **Status**                     | Pass |

## TC003 – Salim Bradley (Payroll Calculation)

N/A due to vaidation error in Creation testing

## TC004 – Bruce Lee (Payroll Calculation)

| Field                          | Value |
|--------------------------------|-------|
| **Test Case ID**               | TC004b |
| **Employee**                   | Bruce Lee |
| **Salary Type**                | Salary |
| **Medical Type**               | Single |
| **Dependents**                 | 1 |
| **Base Salary (per week/hour)**| $4,500.00 |
| **Hours Worked**               | 45 |
| **Saturday Hours**             | 1 |
| **PTO Hours**                  | 0 |
| **Expected Gross Income**      | $4,500.00 |
| **Expected Medical Deduction** | $50.00 |
| **Expected Dependent Stipend** | $45.00 |
| **Expected Taxable Income (TI)** | $4,495.00 |
| **Expected State Tax (3.15%)** | $141.59 |
| **Expected Federal Tax (7.65%)** | $343.87 |
| **Expected Social Security (6.2%)** | $278.69 |
| **Expected Medicare (1.45%)**  | $65.18 |
| **Expected Taxes Owed**        | $829.33 |
| **Expected Net Pay**           | $3,665.67 |
| **Actual Result**              | Values Display as Explected |
| **Screenshot**                 | TC004b.png |
| **Status**                     | Pass |

## TC005 – Edward Elrich Sr. (Payroll Calculation)

| Field                          | Value |
|--------------------------------|-------|
| **Test Case ID**               | TC005b |
| **Employee**                   | Edward Elrich Sr. |
| **Salary Type**                | Salary |
| **Medical Type**               | Family |
| **Dependents**                 | 2 |
| **Base Salary (per week/hour)**| $3,400.00 |
| **Hours Worked**               | 42 |
| **Saturday Hours**             | 1 |
| **PTO Hours**                  | 3 |
| **Expected Gross Income**      | $3,490.00 |
| **Expected Medical Deduction** | $100.00 |
| **Expected Dependent Stipend** | $90.00 (2 × $45) |
| **Expected Taxable Income (TI)** | $3,390.00 |
| **Expected State Tax (3.15%)** | $106.79 |
| **Expected Federal Tax (7.65%)** | $259.33 |
| **Expected Social Security (6.2%)** | $210.18 |
| **Expected Medicare (1.45%)**  | $49.16 |
| **Expected Taxes Owed**        | $625.46 |
| **Expected Net Pay**           | $2,764.55 |
| **Actual Result**              | Values Display as Explected |
| **Screenshot**                 | TC005b.png |
| **Status**                     | Pass |

## TC006 – Riza Hawkeye (Payroll Calculation)

N/A due to validation error in Creation testing

## TC007 – Junji Ito Jr. (Payroll Calculation)

| Field                          | Value |
|--------------------------------|-------|
| **Test Case ID**               | TC007b |
| **Employee**                   | Junji Ito |
| **Salary Type**                | Hourly |
| **Medical Type**               | Single |
| **Dependents**                 | 0 |
| **Base Salary (per hour)**     | $20.00 |
| **Hours Worked**               | 40 |
| **Saturday Hours**             | 0 |
| **PTO Hours**                  | 0 |
| **Expected Gross Income**      | $800.00 |
| **Expected Medical Deduction** | $50.00 |
| **Expected Dependent Stipend** | $0.00 |
| **Expected Taxable Income (TI)** | $750.00 |
| **Expected State Tax (3.15%)** | $23.62 |
| **Expected Federal Tax (7.65%)** | $57.38 |
| **Expected Social Security (6.2%)** | $46.50 |
| **Expected Medicare (1.45%)**  | $10.88 |
| **Expected Taxes Owed**        | $138.38 |
| **Expected Net Pay**           | $611.63 |
| **Actual Result**              | Values Display as Explected |
| **Screenshot**                 | TC007b.png |
| **Status**                     | Pass |

## TC008 – Sir Ken Kaneki (Payroll Calculation)

| Field                          | Value |
|--------------------------------|-------|
| **Test Case ID**               | TC008b |
| **Employee**                   | Ken Kaneki |
| **Salary Type**                | Hourly |
| **Medical Type**               | Family |
| **Dependents**                 | 0 |
| **Base Salary (per hour)**     | $45.00 |
| **Hours Worked**               | 40 |
| **Saturday Hours**             | 2 |
| **PTO Hours**                  | 0 |
| **Expected Gross Income**      | $1,980.00 |
| **Expected Medical Deduction** | $100.00 |
| **Expected Dependent Stipend** | $45.00 |
| **Expected Taxable Income (TI)** | $1,880.00 |
| **Expected State Tax (3.15%)** | $59.22 |
| **Expected Federal Tax (7.65%)** | $143.82 |
| **Expected Social Security (6.2%)** | $116.56 |
| **Expected Medicare (1.45%)**  | $27.26 |
| **Expected Taxes Owed**        | $346.86 |
| **Expected Net Pay**           | $1,533.14 |
| **Actual Result**              | Values Display as Explected |
| **Screenshot**                 | TC008.png |
| **Status**                     | Pass |

## TC009 – Toji Fushiguro (Payroll Calculation)

| Field                          | Value |
|--------------------------------|-------|
| **Test Case ID**               | TC009b |
| **Employee**                   | Toji Fushiguro |
| **Salary Type**                | Hourly |
| **Medical Type**               | Single |
| **Dependents**                 | 1 |
| **Base Salary (per hour)**     | $30.00 |
| **Hours Worked**               | 43 |
| **Saturday Hours**             | 2 |
| **PTO Hours**                  | 0 |
| **Expected Gross Income**      | $1,245.00 |
| **Expected Medical Deduction** | $50.00 |
| **Expected Dependent Stipend** | $45.00 (1 × $45) |
| **Expected Taxable Income (TI)** | $1,245.00 |
| **Expected State Tax (3.15%)** | $37.64 |
| **Expected Federal Tax (7.65%)** | $91.42 |
| **Expected Social Security (6.2%)** | $74.09 |
| **Expected Medicare (1.45%)**  | $17.33 |
| **Expected Taxes Owed**        | $220.48 |
| **Expected Net Pay**           | $974.52 |
| **Actual Result**              | Values Display as Explected |
| **Screenshot**                 | TC009b.png |
| **Status**                     | Pass |

## TC010 – Ken Kuroko (Payroll Calculation)

| Field                          | Value |
|--------------------------------|-------|
| **Test Case ID**               | TC010b |
| **Employee**                   | Ken Kuroko |
| **Salary Type**                | Hourly |
| **Medical Type**               | Family |
| **Dependents**                 | 2 |
| **Base Salary (per hour)**     | $35.50 |
| **Hours Worked**               | 24 |
| **Saturday Hours**             | 0 |
| **PTO Hours**                  | 16 |
| **Expected Gross Income**      | $1,510.00|
| **Expected Medical Deduction** | $100.00 |
| **Expected Dependent Stipend** | $90.00 (2 × $45) |
| **Expected Taxable Income (TI)** | $1,510.00 |
| **Expected State Tax (3.15%)** | $44.41 |
| **Expected Federal Tax (7.65%)** | $107.86 |
| **Expected Social Security (6.2%)** | $87.42 |
| **Expected Medicare (1.45%)**  | $20.45 |
| **Expected Taxes Owed**        | $260.14 |
| **Expected Net Pay**           | $1149.86 |
| **Actual Result**              | Values Display as Explected |
| **Screenshot**                 | TC010b.png |
| **Status**                     | Pass |

## TC011 – Eto Yoshimura (Payroll Calculation)

N/A due to being terminated

## TC012 – Juuzou Suzuya (Payroll Calculation)

N/A due to validation error during Creation testing

## Login Validation Tests

## LOGIN001 – Roy Mustang (Employee Login – Valid)

| Field            | Value |
|------------------|-------|
| **Test Case ID** | LOGIN001 |
| **Employee**     | Roy Mustang |
| **Scenario**     | Login with valid credentials |
| **Input Data**   | Username: <rmustang01@abc.com>, Password:as generated by program |
| **Expected Result** | System grants access, dashboard loads successfully |
| **Actual Result**   | System grants access, dashboard loads successfully  |
| **Screenshot**      | LOGIN001.png |
| **Status**          | Pass |

## LOGIN002 – Roy Mustang (Employee Login – Missing Username)

| Field            | Value |
|------------------|-------|
| **Test Case ID** | LOGIN002 |
| **Employee**     | Roy Mustang |
| **Scenario**     | Login attempt with missing username |
| **Input Data**   | Username: [blank], Password: as generated by program |
| **Expected Result** | Error message displayed: "Username is required" |
| **Actual Result**   | Error message displayed: "Username is required"  |
| **Screenshot**      | LOGIN002.png |
| **Status**          | Pass |

## LOGIN003 – Roy Mustang (Employee Login - Invalid Username)

| Field            | Value |
|------------------|-------|
| **Test Case ID** | LOGIN003 |
| **Employee**     | Roy Mustang |
| **Scenario**     | Login attempt with wrong username |
| **Input Data**   | Username: <rmustang99@abc.com>, Password:as generated by program |
| **Expected Result** | Error message displayed: "Invalid username or password" |
| **Actual Result**   | Error message displayed: "Invalid username or password" |
| **Screenshot**      | LOGIN003_004_008_009.png |
| **Status**          | Pass |

## LOGIN004 – Roy Mustang (Employee Login - Invalid Password)

| Field            | Value |
|------------------|-------|
| **Test Case ID** | LOGIN004 |
| **Employee**     | Roy Mustang |
| **Scenario**     | Login attempt with wrong password |
| **Input Data**   | Username: <rmustang01@abc.com>, Password: WrongPass123 |
| **Expected Result** | Error message displayed: "Invalid username or password" |
| **Actual Result**   | Error message displayed: "Invalid username or password" |
| **Screenshot**      | LOGIN003_004_008_009.png |
| **Status**          | Pass |

## LOGIN005 – Roy Mustang (Employee Login - Missing Password)

| Field            | Value |
|------------------|-------|
| **Test Case ID** | LOGIN005 |
| **Employee**     | Roy Mustang |
| **Scenario**     | Login attempt with missing password |
| **Input Data**   | Username: <rmustang01@abc.com>, Password: [blank] |
| **Expected Result** | Error message displayed: "Password is required" |
| **Actual Result**   | Error message displayed: "Password is required" |
| **Screenshot**      | LOGIN005.png |
| **Status**          | Pass |

## LOGIN006 – Admin Login (Valid)

| Field            | Value |
|------------------|-------|
| **Test Case ID** | LOGIN006 |
| **User Role**    | Admin |
| **Scenario**     | Login with valid admin credentials |
| **Input Data**   | Username: HR0001, Password: AbccoTeam3 |
| **Expected Result** | System grants access to admin dashboard with elevated privileges |
| **Actual Result**   | System grants access to admin dashboard with elevated privileges |
| **Screenshot**      | LOGIN006.png |
| **Status**          | Pass |

## LOGIN007 – Admin Login (Missing Password)

| Field            | Value |
|------------------|-------|
| **Test Case ID** | LOGIN007 |
| **User Role**    | Admin |
| **Scenario**     | Login attempt with missing password |
| **Input Data**   | Username: HR0001, Password: [blank] |
| **Expected Result** | Error message displayed: "Password is required" |
| **Actual Result**   | Error message displayed: "Password is required" |
| **Screenshot**      | LOGIN007.png |
| **Status**          | Pass |

## LOGIN008 – Admin Login (Wrong Password)

| Field            | Value |
|------------------|-------|
| **Test Case ID** | LOGIN008 |
| **User Role**    | Admin |
| **Scenario**     | Login attempt with wrong password |
| **Input Data**   | Username: HR0001, Password: WrongAdmin123 |
| **Expected Result** | Error message displayed: "Invalid username or password" |
| **Actual Result**   | Error message displayed: "Invalid username or password" |
| **Screenshot**      | LOGIN003_004_008_009.png |
| **Status**          | Pass |

## LOGIN009 – Admin Login (Wrong Username)

| Field            | Value |
|------------------|-------|
| **Test Case ID** | LOGIN009 |
| **User Role**    | Admin |
| **Scenario**     | Login attempt with wrong username |
| **Input Data**   | Username: HR9999, Password: AbccoTeam3 |
| **Expected Result** | Error message displayed: "Invalid username or password" |
| **Actual Result**   | Error message displayed: "Invalid username or password" |
| **Screenshot**      | LOGIN003_004_008_009.png |
| **Status**          | Pass |

## LOGIN010 – Admin Login (Missing Username)

| Field            | Value |
|------------------|-------|
| **Test Case ID** | LOGIN010 |
| **User Role**    | Admin |
| **Scenario**     | Login attempt with missing username |
| **Input Data**   | Username: [blank], Password: AbccoTeam3 |
| **Expected Result** | Error message displayed: "Username is required" |
| **Actual Result**   | Error message displayed: "Username is required" |
| **Screenshot**      | LOGIN010.png |
| **Status**          | Pass |

## Admin Generation Test

## ADMIN001 – Admin Report (Total Gross & Net Income)

| Field                          | Value |
|--------------------------------|-------|
| **Test Case ID**               | ADMIN001 |
| **User Role**                  | Admin |
| **Scenario**                   | Verify total gross and net income across passed employees |
| **Input Data**                 | fabricated employee profiles with payroll calculations that passed creation |
| **Expected Total Gross Income**| $23,906.50 |
| **Expected Total Net Income**  | $19,495.70 |
| **Expected Result**            | Admin dashboard/report displays correct totals matching calculated sums and allows saving as a file |
| **Actual Result**              | Admin dashboard/report displays correct totals matching calculated sums and allows saving as a file - Values differ due to errors in Test Log Data (Updated now and accurate display) |
| **Screenshot**                 | ADMIN001.png |
| **Status**                     | Pass |
