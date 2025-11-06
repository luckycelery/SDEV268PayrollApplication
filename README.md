abc-payroll-python/
│
├── README.md                      # Project overview, setup instructions, feature list
├── .gitignore                     # Ignore virtual env, __pycache__, etc.
│
├── /src/                          # Python source code
│   ├── /ui/                       # UI logic (Tkinter or Flask views)
│   ├── /models/                   # Data models (Employee, Payroll, etc.)
│   ├── /controllers/              # Business logic and validation
│   ├── /utils/                    # Helper functions (e.g., tax calculations)
│   └── main.py                    # Entry point
│
├── /database/                     # Database files and schema
│   ├── payroll.db                 # SQLite database
│   └── schema.sql                 # SQL schema (optional)
│
├── /docs/                         # Documentation
│   ├── project-plan.md            # Step-by-step development plan
│   ├── uml-diagrams/              # UML diagrams for actors and classes
│   ├── user-guide.md              # User-friendly documentation
│   ├── security.md                # Security protocols and login logic
│   └── weekly-tasks.md            # 8-week breakdown
│
├── /testing/                      # Testing logs and screenshots
│   ├── initial-testing-log.md     # Pre-testing checklist
│   ├── final-testing-log.md       # Completed test results
│   ├── screenshots/               # Error messages, passed test cases
│   └── test-cases.xlsx            # Structured test matrix
│
├── /data/                         # Demo data for testing
│   ├── employee_profiles.xlsx     # 12 fictional employees
│   └── addresses.xlsx             # Mock addresses
│
└── /submission/                   # Final deliverables
    ├── payroll-report.pdf         # HR sign-off report
    └── payroll-output.txt         # Final payroll file for printing


tables: employees: personal info, job title, pay type, etc.

addresses: linked to employee ID

time_entries: daily hours, PTO, overtime

payroll: salary, deductions, taxes, net pay

users: login credentials and roles (admin, employee)

{MISC INFO ABOUT PROJECT AND REQUIREMENTS}
* will use sql lite
* HR001 admin cred with secure pw

* need to dev UML diagrams
* sketch designs finalize and input into user doc 
* need to create template for project plan combined (include types of algorithms used) - with user doc (use past one for reference)
                * Develop a detailed plan outlining the steps you will use to create your
                  program. This should include the number of menus, and screens required,
                  database creation and the type of database you use in your project and what
                  algorithms will be employed in the development project, providing a rationale
                  for their selection.
                o You will need to identify the types of actors that will use your application and
                  produce UML diagrams for all actors involved in the application to clearly
                  define their roles and responsibilities.
                o Include a breakdown of tasks to be completed over the next eight weeks as
                  part of the project plan.
                o Prepare user-friendly documentation for the application to facilitate user
                  understanding of its features and functionalities.
                o Follow good program standards by storing and defining your variables
                  establishing security and how you will be protecting the sensitive data entered
                  in the payroll system
                * proof of security measures included in this too - probalby will be a screenshot
                * Your plan should carefully detail the structure and organization of the
                database to guarantee optimal functionality.
                  


* develop testing log based on UML diagrams to test different scenarious methodically
              * Establish a structured testing log to methodically test the application's various
                  scenarios. Your testing log should be thoroughly checked to make sure there
                  is validation in place to protect the user from making errors.
              o Use the testing log to verify the accuracy of all calculations in the application,
                  particularly in relation to employee payments and taxes. You should provide
                  screenshots where you can show that your testing scenarios passed. For
                  example, your screenshot should display error messages, etc.
              o Create a minimum of 12 fabricated employee profiles within the application for
                  testing and demonstration purposes.
              o Your documentation posted in GitHub should contain your initial testing log
                  and then a completed log to show your log was available before the testing
                  began.

The main screen should feature the following options:
1. Login
2. User ID and Password Entry
3. User Type Selection (Admin or Employee)
4. Exit Program
Once a user has successfully logged in:
- For Admin users:
- Employee demographics access
- Payroll information access / Calculate payroll
- Adding, editing, and deleting options available
- Employee search function
- Reporting
- Application information (version number)
- For Employee users:
- Hours worked entry functionality
- PTO (personal time off) option
- Paycheck calculation feature
As the project progresses, new steps and updates will be integrated into each module,
enhancing, and refining the plan based on knowledge gained from previous and current
courses.
Employee Screen
• Only accessible by the admin login.
• Adding, editing, or deleting an employee record
• Fields that are required and should apply appropriate validation.
o Employee ID
o Department, Job Title
o First Name, Last Name, Sur Name
o Status (active or terminated)
o Date of Birth (must be at least 18 years of age)
o Gender (Male or Female)
o Pay type (Salary or Hourly)
o Company email
o Address Line 1, Address Line 2
o City, State, or Zip
o Employee picture when available
Salary Screen
• Only accessible by the admin login.
• Current information should be displayed on the screen to support any salary.
o Department
o Job Type Title
o First Name and Last Name
o Status
o Date Hire
o Salary Type
o Base Salary
o Medical (Single or Family Coverage)
o # of Dependents
Make sure you include the appropriate validations and checks. Items listed are the
minimum validations.
Employee Time Entry Screen
• Add by the employee.
• Edit until the payroll has been submitted.
• Admin - can adjust based on issues with previous payrolls.
• If the employee's pay is salary,
o The only entry will be to add PTO. Otherwise, they should
automatically be paid 8 hours on Monday or Friday.
• If the employee's pay is hourly,
o The employee should be able to enter the total number for the day.
o the system should calculate overtime based on an 8-hour-a-day
(anything over 8 hours should pay time and a half.
o The system should be able to collect hours worked for 7 days
(anytime on Saturday should pay time and a half.
• Medical is calculated at $50 for single coverage and $100 for family
coverage.
• The employee is given a $45 stipend for each dependent.
• The screen should show the employee's medical, dependent stipend, taxes
for state, federal, Medicare, and social security deduction amounts for both
the employee and the employer.
• State tax, IN 3.15%
• Federal tax Employee 7.65%, Employer 7.65%
• Social Security tax Employee 6.2%, Employer 6.2%
• Medicare Employee 1.45%, Employer 1.45%
Admin Options and Calculating Payroll
• Only accessible by the admin login
• Calculate the payroll.
o Lock the work entry so there are no updates after the calculated payroll
has been selected.
o Calculate the gross payroll.
o Calculate the net payroll.
o Create a report for HR to sign off.
o Create a file for the payroll department to see to the printer after sign-off.
Hint: all deductions should be on a pretax basis, i.e., the medical should be deducted
before calculating state, federal, or other taxes.
* The program should include arrays or lists
for managing data entry, insertion, and deletion, demonstrating your proficiency in the
techniques covered in the course. Showcase your dedication and skills as you develop
this application.

A comprehensive plan must be established to begin the payroll program's development
process. This plan should include tasks such as collecting hours worked, calculating
taxes, designing the screens, determining the information to be captured, designing the
database, and other relevant activities. It is crucial to review all input data and identify
any inconsistencies carefully. For instance, if the standard work hours are 40 hours per
week, submitting 80 hours would be considered unusual and should be addressed
promptly.
A minimum of twelve employees should be designated for use in test cases. Your
responsibilities will involve creating documentation to support the development plan and
providing guidance to users after the application is completed. Additionally, you will be
responsible for designing and developing the Java-based application.
All program files and documentation should be organized within GitHub. Your final
submission will be a link to your GitHub repository, where the instructor will grade your
project. Make sure you give your instructor access to your GitHub so there will not be an
access issue when they go to grade the final submissions.



  
