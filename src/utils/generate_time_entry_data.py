import csv
from datetime import datetime, timedelta

# All hourly employees (need time entries)
hourly_employees = ['E007', 'E008', 'E009', 'E010', 'E013']

# Date range: Sept 29 - Nov 30, 2025
start_date = datetime(2025, 9, 29)
end_date = datetime(2025, 11, 30)

entries = []
entries.append(['employee_id', 'work_date', 'hours_worked', 'pto_hours'])

current_date = start_date
while current_date <= end_date:
    # Skip weekends
    if current_date.weekday() < 5:  # Monday=0, Friday=4
        for emp_id in hourly_employees:
            # Thanksgiving week (Nov 24-28)
            if current_date.month == 11 and 27 <= current_date.day <= 28:
                # Thanksgiving holiday - PTO
                entries.append([emp_id, current_date.strftime('%Y-%m-%d'), '0', '8.0'])
            else:
                # Regular workday - 8 hours (with some variation)
                if emp_id == 'E008':
                    # E008 sometimes works overtime
                    hours = 10.0 if current_date.day % 7 == 0 else 8.0
                elif emp_id == 'E009':
                    # E009 occasionally works less
                    hours = 6.0 if current_date.day % 11 == 0 else 8.0
                else:
                    hours = 8.0
                entries.append([emp_id, current_date.strftime('%Y-%m-%d'), str(hours), '0'])

    current_date += timedelta(days=1)

# Write to CSV
with open('data/sample_time_entries.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(entries)

print(f'Generated {len(entries) - 1} time entries')
