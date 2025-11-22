# Payroll Application Testing Log

## Initial Log

## Profile Creation Tests

| Test Case ID | Employee | Scenario | Input Data | Expected Result | Actual Result | Screenshot | Status |
|--------------|----------|----------|------------|----------------|---------------|------------|--------|
| TC001a       | Roy Mustang | Add Employee Profile | Full profile data entered | Profile saved successfully | Pending | Pending | Pending |
| TC002a       | Alfonse Elrich | Add Employee Profile | Full profile data entered | Profile saved successfully | Pending | Pending | Pending |
| TC003a       | Salim Bradley | Add Employee Profile | Full profile data entered | Error Message: Age under 18 | Pending | Pending | Pending |
| TC004a       | Bruce Lee |  Add Employee Profile | Full profile data entered - DOB under 18 | Error Message: Age under 18 | Pending | Pending | Pending |
| TC005a       | Edward Elrich Sr. |  Add Employee Profile | Full profile data entered | Profile saved successfully | Pending | Pending | Pending |
| TC006a       | Riza Hawkeye |  Add Employee Profile | Full profile data entered - no gender endtered| Error Message: Gender must be entered | Pending | Pending | Pending |
| TC007a       | Junji Ito Jr. | Add Employee Profile | Full profile data entered | Profile saved successfully | Pending | Pending | Pending |
| TC008a       | Sir Ken Kaneki | Add Employee Profile | Full profile data entered | Profile saved successfully | Pending | Pending | Pending |
| TC009a       | Toki Fushiguro | Add Employee Profile | Full profile data entered | Profile saved successfully | Pending | Pending | Pending |
| TC010a       | Ken Kuroko | Add Employee Profile | Full profile data entered | Profile saved successfully | Pending | Pending | Pending |
| TC011a       | Eto Yoshimura | Add Employee Profile | Full profile data entered | Profile saved successfully | Pending | Pending | Pending |
| TC012a       | Juuzou Suzuya | Add Employee Profile | Full profile data entered - start date after present| Error Message: Start Date must be before or at today's date| Pending | Pending | Pending |

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
| **Expected State Tax (3.15%)** | $92.93 |
| **Expected Federal Tax (7.65%)** | $225.68 |
| **Expected Social Security (6.2%)** | $182.90 |
| **Expected Medicare (1.45%)**  | $42.78 |
| **Expected Taxes Owed**        | $544.28 |
| **Expected Net Pay**           | $2,405.73 |
| **Expected Employer Fed Tax (7.65%)** | $225.68 |
| **Expected Employer SS Tax (6.2%)** | $182.90 |
| **Expected Employer Medicare Tax (1.45%)** | $42.78 |
| **Actual Result**              | Pending |
| **Screenshot**                 | Pending |
| **Status**                     | Pending |

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
| **Expected Gross Income**      | $5,000.00 |
| **Expected Medical Deduction** | $50.00 |
| **Expected Dependent Stipend** | $0.00 |
| **Expected Taxable Income (TI)** | $4,950.00 |
| **Expected State Tax (3.15%)** | $155.93 |
| **Expected Federal Tax (7.65%)** | $378.68 |
| **Expected Social Security (6.2%)** | $306.90 |
| **Expected Medicare (1.45%)**  | $71.78 |
| **Expected Taxes Owed**        | $913.28 |
| **Expected Net Pay**           | $4,036.73 |
| **Expected Employer Fed Tax (7.65%)** | $378.68 |
| **Expected Employer SS Tax (6.2%)** | $306.90 |
| **Expected Employer Medicare Tax (1.45%)** | $71.78 |
| **Actual Result**              | Pending |
| **Screenshot**                 | Pending |
| **Status**                     | Pending |

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
| **Expected Employer Fed Tax (7.65%)** | $343.87 |
| **Expected Employer SS Tax (6.2%)** | $278.69 |
| **Expected Employer Medicare Tax (1.45%)** | $65.18 |
| **Actual Result**              | Pending |
| **Screenshot**                 | Pending |
| **Status**                     | Pending |

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
| **Expected Gross Income**      | $3,400.00 |
| **Expected Medical Deduction** | $100.00 |
| **Expected Dependent Stipend** | $90.00 (2 × $45) |
| **Expected Taxable Income (TI)** | $3,390.00 |
| **Expected State Tax (3.15%)** | $106.79 |
| **Expected Federal Tax (7.65%)** | $259.34 |
| **Expected Social Security (6.2%)** | $210.18 |
| **Expected Medicare (1.45%)**  | $49.16 |
| **Expected Taxes Owed**        | $625.46 |
| **Expected Net Pay**           | $2,764.55 |
| **Expected Employer Fed Tax (7.65%)** | $259.34 |
| **Expected Employer SS Tax (6.2%)** | $210.18 |
| **Expected Employer Medicare Tax (1.45%)** | $49.16 |
| **Actual Result**              | Pending |
| **Screenshot**                 | Pending |
| **Status**                     | Pending |

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
| **Hours Worked**               | 38 |
| **Saturday Hours**             | 2 |
| **PTO Hours**                  | 0 |
| **Expected Gross Income**      | $780.00 |
| **Expected Medical Deduction** | $50.00 |
| **Expected Dependent Stipend** | $0.00 |
| **Expected Taxable Income (TI)** | $730.00 |
| **Expected State Tax (3.15%)** | $23.00 |
| **Expected Federal Tax (7.65%)** | $55.85 |
| **Expected Social Security (6.2%)** | $45.26 |
| **Expected Medicare (1.45%)**  | $10.59 |
| **Expected Taxes Owed**        | $134.69 |
| **Expected Net Pay**           | $595.32 |
| **Expected Employer Fed Tax (7.65%)** | $55.85 |
| **Expected Employer SS Tax (6.2%)** | $45.26 |
| **Expected Employer Medicare Tax (1.45%)** | $10.59 |
| **Actual Result**              | Pending |
| **Screenshot**                 | Pending |
| **Status**                     | Pending |

## TC008 – Sir Ken Kaneki (Payroll Calculation)

| Field                          | Value |
|--------------------------------|-------|
| **Test Case ID**               | TC008b |
| **Employee**                   | Ken Kaneki |
| **Salary Type**                | Hourly |
| **Medical Type**               | Family |
| **Dependents**                 | 0 |
| **Base Salary (per hour)**     | $45.00 |
| **Hours Worked**               | 37 |
| **Saturday Hours**             | 0 |
| **PTO Hours**                  | 2 |
| **Expected Gross Income**      | $1,755.00 |
| **Expected Medical Deduction** | $100.00 |
| **Expected Dependent Stipend** | $0.00 |
| **Expected Taxable Income (TI)** | $1,655.00 |
| **Expected State Tax (3.15%)** | $52.13 |
| **Expected Federal Tax (7.65%)** | $126.61 |
| **Expected Social Security (6.2%)** | $102.61 |
| **Expected Medicare (1.45%)**  | $24.00 |
| **Expected Taxes Owed**        | $305.35 |
| **Expected Net Pay**           | $1,349.65 |
| **Expected Employer Fed Tax (7.65%)** | $126.61 |
| **Expected Employer SS Tax (6.2%)** | $102.61 |
| **Expected Employer Medicare Tax (1.45%)** | $24.00 |
| **Actual Result**              | Pending |
| **Screenshot**                 | Pending |
| **Status**                     | Pending |

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
| **Expected Gross Income**      | $1,275.00 |
| **Expected Medical Deduction** | $50.00 |
| **Expected Dependent Stipend** | $45.00 (1 × $45) |
| **Expected Taxable Income (TI)** | $1,270.00 |
| **Expected State Tax (3.15%)** | $40.01 |
| **Expected Federal Tax (7.65%)** | $97.16 |
| **Expected Social Security (6.2%)** | $78.74 |
| **Expected Medicare (1.45%)**  | $18.42 |
| **Expected Taxes Owed**        | $234.32 |
| **Expected Net Pay**           | $1,035.69 |
| **Expected Employer Fed Tax (7.65%)** | $97.16 |
| **Expected Employer SS Tax (6.2%)** | $78.74 |
| **Expected Employer Medicare Tax (1.45%)** | $18.42 |
| **Actual Result**              | Pending |
| **Screenshot**                 | Pending |
| **Status**                     | Pending |

## TC010 – Ken Kuroko (Payroll Calculation)

| Field                          | Value |
|--------------------------------|-------|
| **Test Case ID**               | TC010b |
| **Employee**                   | Ken Kuroko |
| **Salary Type**                | Hourly |
| **Medical Type**               | Family |
| **Dependents**                 | 2 |
| **Base Salary (per hour)**     | $35.50 |
| **Hours Worked**               | 41 |
| **Saturday Hours**             | 2 |
| **PTO Hours**                  | 2 |
| **Expected Gross Income**      | $1,526.50 |
| **Expected Medical Deduction** | $100.00 |
| **Expected Dependent Stipend** | $90.00 (2 × $45) |
| **Expected Taxable Income (TI)** | $1,516.50 |
| **Expected State Tax (3.15%)** | $47.77 |
| **Expected Federal Tax (7.65%)** | $116.01 |
| **Expected Social Security (6.2%)** | $94.02 |
| **Expected Medicare (1.45%)**  | $21.99 |
| **Expected Taxes Owed**        | $279.79 |
| **Expected Net Pay**           | $1,236.71 |
| **Expected Employer Fed Tax (7.65%)** | $116.01 |
| **Expected Employer SS Tax (6.2%)** | $94.02 |
| **Expected Employer Medicare Tax (1.45%)** | $21.99 |
| **Actual Result**              | Pending |
| **Screenshot**                 | Pending |
| **Status**                     | Pending |

## TC011 – Eto Yoshimura (Payroll Calculation)

| Field                          | Value |
|--------------------------------|-------|
| **Test Case ID**               | TC011b |
| **Employee**                   | Eto Yoshimura |
| **Salary Type**                | Salary |
| **Medical Type**               | Single |
| **Dependents**                 | 0 |
| **Base Salary (per week)**     | $3,000.00 |
| **Hours Worked**               | 40 |
| **Saturday Hours**             | 0 |
| **PTO Hours**                  | 4 |
| **Expected Gross Income**      | $3,000.00 |
| **Expected Medical Deduction** | $50.00 |
| **Expected Dependent Stipend** | $0.00 |
| **Expected Taxable Income (TI)** | $2,950.00 |
| **Expected State Tax (3.15%)** | $92.93 |
| **Expected Federal Tax (7.65%)** | $225.68 |
| **Expected Social Security (6.2%)** | $182.90 |
| **Expected Medicare (1.45%)**  | $42.78 |
| **Expected Taxes Owed**        | $544.28 |
| **Expected Net Pay**           | $2,405.73 |
| **Expected Employer Fed Tax (7.65%)** | $225.68 |
| **Expected Employer SS Tax (6.2%)** | $182.90 |
| **Expected Employer Medicare Tax (1.45%)** | $42.78 |
| **Actual Result**              | Pending |
| **Screenshot**                 | Pending |
| **Status**                     | Pending |

## TC012 – Juuzou Suzuya (Payroll Calculation)
N/A due to validation error during Creation testing

## Login Validation Tests

## LOGIN001 – Roy Mustang (Employee Login – Valid)

| Field            | Value |
|------------------|-------|
| **Test Case ID** | LOGIN001 |
| **Employee**     | Roy Mustang |
| **Scenario**     | Login with valid credentials |
| **Input Data**   | Username: rmustang01@abc.com, Password:as generated by program |
| **Expected Result** | System grants access, dashboard loads successfully |
| **Actual Result**   | Pending |
| **Screenshot**      | Pending |
| **Status**          | Pending |

## LOGIN002 – Roy Mustang (Employee Login – Missing Username)

| Field            | Value |
|------------------|-------|
| **Test Case ID** | LOGIN002 |
| **Employee**     | Roy Mustang |
| **Scenario**     | Login attempt with missing username |
| **Input Data**   | Username: [blank], Password: as generated by program |
| **Expected Result** | Error message displayed: "Username is required" |
| **Actual Result**   | Pending |
| **Screenshot**      | Pending |
| **Status**          | Pending |

## LOGIN003 – Roy Mustang (Employee Login - Invalid Username)

| Field            | Value |
|------------------|-------|
| **Test Case ID** | LOGIN003 |
| **Employee**     | Roy Mustang |
| **Scenario**     | Login attempt with wrong username |
| **Input Data**   | Username: rmustang99@abc.com, Password:as generated by program |
| **Expected Result** | Error message displayed: "Invalid username or password" |
| **Actual Result**   | Pending |
| **Screenshot**      | Pending |
| **Status**          | Pending |

## LOGIN004 – Roy Mustang (Employee Login - Invalid Password)

| Field            | Value |
|------------------|-------|
| **Test Case ID** | LOGIN004 |
| **Employee**     | Roy Mustang |
| **Scenario**     | Login attempt with wrong password |
| **Input Data**   | Username: rmustang01@abc.com, Password: WrongPass123 |
| **Expected Result** | Error message displayed: "Invalid username or password" |
| **Actual Result**   | Pending |
| **Screenshot**      | Pending |
| **Status**          | Pending |

## LOGIN005 – Roy Mustang (Employee Login - Missing Password)

| Field            | Value |
|------------------|-------|
| **Test Case ID** | LOGIN005 |
| **Employee**     | Roy Mustang |
| **Scenario**     | Login attempt with missing password |
| **Input Data**   | Username: rmustang01@abc.com, Password: [blank] |
| **Expected Result** | Error message displayed: "Password is required" |
| **Actual Result**   | Pending |
| **Screenshot**      | Pending |
| **Status**          | Pending |

## LOGIN006 – Admin Login (Valid)

| Field            | Value |
|------------------|-------|
| **Test Case ID** | LOGIN006 |
| **User Role**    | Admin |
| **Scenario**     | Login with valid admin credentials |
| **Input Data**   | Username: HR0001, Password: AbccoTeam3 |
| **Expected Result** | System grants access to admin dashboard with elevated privileges |
| **Actual Result**   | Pending |
| **Screenshot**      | Pending |
| **Status**          | Pending |

## LOGIN007 – Admin Login (Missing Password)

| Field            | Value |
|------------------|-------|
| **Test Case ID** | LOGIN007 |
| **User Role**    | Admin |
| **Scenario**     | Login attempt with missing password |
| **Input Data**   | Username: HR0001, Password: [blank] |
| **Expected Result** | Error message displayed: "Password is required" |
| **Actual Result**   | Pending |
| **Screenshot**      | Pending |
| **Status**          | Pending |

## LOGIN008 – Admin Login (Wrong Password)

| Field            | Value |
|------------------|-------|
| **Test Case ID** | LOGIN008 |
| **User Role**    | Admin |
| **Scenario**     | Login attempt with wrong password |
| **Input Data**   | Username: HR0001, Password: WrongAdmin123 |
| **Expected Result** | Error message displayed: "Invalid username or password" |
| **Actual Result**   | Pending |
| **Screenshot**      | Pending |
| **Status**          | Pending |

## LOGIN009 – Admin Login (Wrong Username)

| Field            | Value |
|------------------|-------|
| **Test Case ID** | LOGIN009 |
| **User Role**    | Admin |
| **Scenario**     | Login attempt with wrong username |
| **Input Data**   | Username: HR9999, Password: AbcCoGroup3'25 |
| **Expected Result** | Error message displayed: "Invalid username or password" |
| **Actual Result**   | Pending |
| **Screenshot**      | Pending |
| **Status**          | Pending |

## LOGIN010 – Admin Login (Missing Username)

| Field            | Value |
|------------------|-------|
| **Test Case ID** | LOGIN010 |
| **User Role**    | Admin |
| **Scenario**     | Login attempt with missing username |
| **Input Data**   | Username: [blank], Password: AbcCoGroup3'25 |
| **Expected Result** | Error message displayed: "Username is required" |
| **Actual Result**   | Pending |
| **Screenshot**      | Pending |
| **Status**          | Pending |

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
| **Actual Result**              | Pending |
| **Screenshot**                 | Pending |
| **Status**                     | Pending |




