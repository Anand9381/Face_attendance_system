import csv
import os
from datetime import datetime

DATA_DIR = "data"
FILE = os.path.join(DATA_DIR, "attendance.csv")

def init_attendance():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(FILE):
        with open(FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Employee ID",
                "Employee Name",
                "Date",
                "Day",
                "Punch In",
                "Punch Out",
                "Working Duration",
                "Attendance Status"
            ])

def calculate_duration(in_time, out_time):
    fmt = "%H:%M:%S"
    t1 = datetime.strptime(in_time, fmt)
    t2 = datetime.strptime(out_time, fmt)
    return str(t2 - t1)

def generate_emp_id(name):
    return "EMP" + str(abs(hash(name)) % 10000).zfill(4)

def has_punched_in_today(name):
    today = datetime.now().strftime("%Y-%m-%d")

    if not os.path.exists(FILE):
        return False

    with open(FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if row[1] == name and row[2] == today and row[4] != "":
                return True
    return False

def mark_attendance(name, punch):
    date = datetime.now().strftime("%Y-%m-%d")
    day = datetime.now().strftime("%A")
    time = datetime.now().strftime("%H:%M:%S")
    emp_id = generate_emp_id(name)

    rows = []
    with open(FILE, "r") as f:
        rows = list(csv.reader(f))

    if punch == "out" and not has_punched_in_today(name):
        return "NOT_PUNCHED_IN"

    updated = False

    for row in rows[1:]:
        if row[1] == name and row[2] == date:
            if punch == "out":
                row[5] = time
                row[6] = calculate_duration(row[4], row[5])
                row[7] = "Present"
            updated = True

    if not updated and punch == "in":
        rows.append([
            emp_id,
            name,
            date,
            day,
            time,
            "",
            "",
            "In Progress"
        ])

    with open(FILE, "w", newline="") as f:
        csv.writer(f).writerows(rows)

    return "SUCCESS"
