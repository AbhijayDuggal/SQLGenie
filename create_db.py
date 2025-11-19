import sqlite3
import os
import random

DB_PATH = "data/sample.db"

# Some Indian names and cities for realistic data
first_names = ["Aarav", "Vivaan", "Aditya", "Sai", "Arjun", "Ishaan", "Krishna", "Rohan", "Kabir", "Ananya",
               "Saanvi", "Aadhya", "Diya", "Meera", "Ira", "Kavya", "Anika", "Riya", "Sneha", "Pooja"]
last_names = ["Sharma", "Verma", "Singh", "Gupta", "Mehta", "Patel", "Reddy", "Chopra", "Kapoor", "Nair",
              "Joshi", "Agarwal", "Malhotra", "Bhat", "Khan", "Bose", "Desai", "Iyer", "Dutt", "Saxena"]
departments = ["Engineering", "HR", "Finance", "Marketing", "Sales", "Legal", "Operations", "IT Support"]
locations = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad", "Kolkata", "Pune", "Jaipur"]

# Generate random Indian dates
def random_date(start_year=2015, end_year=2025):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"

# SQL commands to create tables and insert 50+ rows
SQL_COMMANDS = """
-- Departments Table
CREATE TABLE departments (
    dept_id INTEGER PRIMARY KEY,
    dept_name TEXT NOT NULL,
    location TEXT
);

-- Employees Table
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    dept_id INTEGER,
    salary REAL NOT NULL,
    hire_date TEXT,
    manager_id INTEGER,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id),
    FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
);
"""

# Function to generate insert statements for departments
def generate_departments():
    inserts = ""
    for i, dept in enumerate(departments, start=1):
        loc = random.choice(locations)
        inserts += f"INSERT INTO departments (dept_id, dept_name, location) VALUES ({i}, '{dept}', '{loc}');\n"
    return inserts

# Function to generate insert statements for employees
def generate_employees(num=50):
    inserts = ""
    for i in range(1, num + 1):
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        dept_id = random.randint(1, len(departments))
        salary = random.randint(30000, 150000)
        hire_date = random_date()
        manager_id = random.randint(1, i) if i > 1 else "NULL"
        inserts += f"INSERT INTO employees (employee_id, first_name, last_name, dept_id, salary, hire_date, manager_id) "
        inserts += f"VALUES ({i}, '{fname}', '{lname}', {dept_id}, {salary}, '{hire_date}', {manager_id if manager_id != 'NULL' else 'NULL'});\n"
    return inserts

# Combine all SQL
SQL_COMMANDS += generate_departments()
SQL_COMMANDS += generate_employees(50)

def create_database():
    """Creates the data/sample.db file and populates it with the schema and data."""
    if not os.path.exists('data'):
        os.makedirs('data')

    try:
        # Delete existing database file to ensure a clean start
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Execute the multi-line SQL commands
        cursor.executescript(SQL_COMMANDS)

        conn.commit()
        conn.close()
        print(f"Successfully created and populated database: {DB_PATH}")

    except sqlite3.Error as e:
        print(f"An error occurred while creating the database: {e}")

if __name__ == "__main__":
    create_database()
