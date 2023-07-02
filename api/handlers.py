import os

from fastapi import APIRouter, File, HTTPException, UploadFile
from prisma.models import Departments, Employees, Jobs

from api.db import CSVModel
from api.lib import Faker, to_timestamp
from api.schemas import (DepartmentCreate, EmployeeCreate, EmployeeFaker,
                         JobCreate)

app = APIRouter(prefix="/api")


async def upload_handler(file: UploadFile = File(...)):
    """Uploads a CSV file and saves it to the static folder"""
    if not file.filename.endswith(".csv"): # type: ignore
        raise HTTPException(status_code=400, detail="File must be a CSV")
    if not os.path.isdir("static"):
        os.mkdir("static")
    contents = await file.read()
    with open(f"static/{file.filename}", "wb") as csv_file:
        csv_file.write(contents)


@app.post("/employees")
async def upload_employees_endpoint(file: UploadFile = File(...)):
    """Converts CSV File to EmployeeCreate instances"""
    try:
        await upload_handler(file)
        models = EmployeeCreate.from_csv(f"static/{file.filename}")
        return await Employees.prisma().create_many(data=[model.dict() for model in models]) # type: ignore
    
    except AssertionError as exc:
        raise HTTPException(
            status_code=400, detail="File must named after the model"
        ) from exc


@app.post("/jobs")
async def upload_jobs_endpoint(file: UploadFile = File(...)):
    """Converts CSV File to JobCreate instances"""
    try:
        assert isinstance(file.filename, str)
        assert file.filename.split(".")[0] == "jobs"
        await upload_handler(file)
        models = JobCreate.from_csv(f"static/{file.filename}")
        await Jobs.prisma().create_many(data=[model.dict() for model in models]) # type: ignore
        response = await Jobs.prisma().find_many()
        return {
            "status": "success",
            "detail": "Jobs created successfully",
            "data": response
        }
    except AssertionError as exc:
        print(exc)
        response = await Jobs.prisma().find_many()
        return {
            "status": "error",
            "detail": "File must named after the model",
            "data": response
        }


@app.post("/departments")
async def upload_departments_endpoint(file: UploadFile = File(...)):
    """Converts CSV File to DepartmentCreate instances"""
    try:
        assert isinstance(file.filename, str)
        assert file.filename.split(".")[0] == "departments"
        await upload_handler(file)
        models = DepartmentCreate.from_csv(f"static/{file.filename}")
        await Departments.prisma().create_many(data=[model.dict() for model in models]) # type: ignore
        response = await Departments.prisma().find_many()
        return {
            "status": "success",
            "detail": "Departments created successfully",
            "data": response
        }
    except AssertionError as exc:
        print(exc)
        response = await Departments.prisma().find_many()
        return {
            "status": "error",
            "detail": "File must named after the model",
            "data": response
        }
        