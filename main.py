"""Main module of the API. Contains the endpoints for the SQL section of the test."""
from collections import defaultdict
from datetime import datetime

from prisma.models import Employees

from api import bootstrap

app = bootstrap()

# Section 2 - SQL


@app.get("/employees/quarterly")
async def employees_quarterly():
    """Number of employees hired for each job and department in 2021 divided by quarter"""

    employees = await Employees.prisma().find_many(
        where={"datetime": {"gte": "2021-01-01T00:00:00", "lt": "2022-01-01T00:00:00"}}
    )

    hires_per_quarter = defaultdict(lambda: defaultdict(int))
    for employee in employees:
        quarter = (datetime.fromisoformat(employee.datetime).month - 1) % 3 + 1
        key = (employee.department, employee.job)
        hires_per_quarter[key][quarter] += 1

    output = []
    for (department, job), quarters in hires_per_quarter.items():
        output.append(
            {
                "department": department,
                "job": job,
                "Q1": quarters.get(1, 0),
                "Q2": quarters.get(2, 0),
                "Q3": quarters.get(3, 0),
                "Q4": quarters.get(4, 0),
            }
        )

    return output


@app.get("/departments/overhiring")
async def departments_overhiring():
    """
    List of ids, name and number of employees hired of each department that hired more
    employees than the mean of employees hired in 2021 for all the departments, ordered
    by the number of employees hired (descending).
    """
    employees = await Employees.prisma().find_many(
        where={"datetime": {"gte": "2021-01-01T00:00:00", "lt": "2022-01-01T00:00:00"}}
    )

    hires_per_department = defaultdict(int)
    for employee in employees:
        hires_per_department[employee.department] += 1

    mean_hires = sum(hires_per_department.values()) / len(hires_per_department)

    above_average_departments = [
        {"id": id, "department": department, "hired": hired}
        for id, (department, hired) in enumerate(hires_per_department.items())
        if hired > mean_hires
    ]

    return above_average_departments
