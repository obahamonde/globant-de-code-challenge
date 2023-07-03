"""Section 1 - API
In the context of a DB migration with 3 different tables (departments, jobs, employees) , create
a local REST API that must:

1. Receive historical data from CSV files
2. Upload these files to the new DB
3. Be able to insert batch transactions (1 up to 1000 rows) with one request
"""
import os
import asyncio
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from prisma.models import Departments, Employees, Jobs

from api.lib import datetime
from api.schemas import (DepartmentCreate, EmployeeCreate, EmployeeFaker,
                         JobCreate, faker)

app = APIRouter(prefix="/api", tags=["csv"])

# 1. Receive historical data from CSV files


async def upload_handler(file: UploadFile = File(...)):
    """Uploads a CSV file and saves it to the static folder"""
    if not file.filename.endswith(".csv"):  # type: ignore
        raise HTTPException(status_code=400, detail="File must be a CSV")
    if not os.path.isdir("static"):
        os.mkdir("static")
    contents = await file.read()
    with open(f"static/{file.filename}", "wb") as csv_file:
        csv_file.write(contents)


#@app.get("/employees/mock")
async def mock_employee_handler():
    """Generates fake data and saves it to a CSV file"""
    _now = datetime.now().isoformat()
    if not os.path.isdir("static"):
        os.mkdir("static")
    data = EmployeeFaker.gen_batch(1000)
    EmployeeFaker.to_csv(_now, data)
    return {
        "status": "success",
        "detail": "Fake data generated successfully",
        "data": data,
    }


#@app.get("/employees")
async def get_employees_endpoint():
    """Returns all employees"""
    return await Employees.prisma().find_many()


# 2. Upload these files to the new DB
# 3. Be able to insert batch transactions (1 up to 1000 rows) with one request

@app.post("/employees")
async def upload_employees_endpoint(file: UploadFile = File(...)):
    """Converts CSV File to EmployeeCreate instances"""
    try:
        await upload_handler(file)
        models = EmployeeCreate.from_csv(f"static/{file.filename}")
        if len(models) > 1000:
            models = models[:1000]
        await asyncio.gather(*[Employees.prisma().create(data=model.dict()) for model in models])
        #return await Employees.prisma().find_many()
        return {
            "status": "success",
            "message": "Employees created successfully",
        }
    except AssertionError as exc:
        print(exc)
        return {
            "status": "error",
            "message": "File must named after the model",
        }

@app.post("/jobs")
async def upload_jobs_endpoint(file: UploadFile = File(...)):
    """Converts CSV File to JobCreate instances"""
    try:
        assert isinstance(file.filename, str)
        assert file.filename.split(".")[0] == "jobs"
        await upload_handler(file)
        models = JobCreate.from_csv(f"static/{file.filename}")
        jobs = await Jobs.prisma().find_many()
        for model in models:
            if model.job not in [job.job for job in jobs]:
                await Jobs.prisma().create(data=model.dict())  # type: ignore
        return await Jobs.prisma().find_many()
    except AssertionError as exc:
        print(exc)
        return {
            "status": "error",
            "message": "File must named after the model",
        }


@app.post("/departments")
async def upload_departments_endpoint(file: UploadFile = File(...)):
    """Converts CSV File to DepartmentCreate instances"""
    try:
        assert isinstance(file.filename, str)
        assert file.filename.split(".")[0] == "departments"
        await upload_handler(file)
        models = DepartmentCreate.from_csv(f"static/{file.filename}")
        departments = await Departments.prisma().find_many()
        for model in models:
            if model.department not in [
                department.department for department in departments
            ]:
                await Departments.prisma().create(data=model.dict())  # type: ignore
        return await Departments.prisma().find_many()
    except AssertionError as exc:
        print(exc)
        return {
            "status": "error",
            "detail": "File must named after the model"
        }

# Some extra endpoints for operational purposes disabled by default

#@app.delete("/employees")
async def delete_employees_endpoint():
    """Deletes all employees"""
    return await Employees.prisma().delete_many()


#@app.get("/jobs")
async def get_jobs_endpoint():
    """Returns all jobs"""
    return await Jobs.prisma().find_many(include={"employees": True})


#@app.delete("/jobs")
async def delete_jobs_endpoint():
    """Deletes all jobs"""
    return await Jobs.prisma().delete_many()


#@app.get("/departments")
async def get_departments_endpoint():
    """Returns all departments"""
    return await Departments.prisma().find_many(include={"employees": True})


#@app.delete("/departments")
async def delete_departments_endpoint():
    """Deletes all departments"""
    return await Departments.prisma().delete_many()

# Populates the faker instance with the Jobs and Departments data from the DB

@app.on_event("startup")
async def startup_event():
    """Runs the Faker"""
    await faker.run()

# Redirects to the docs [TODO: Add a frontend to the API]

@app.get("/")
async def index():
    """Entry point for the API"""
    return RedirectResponse("/docs")
