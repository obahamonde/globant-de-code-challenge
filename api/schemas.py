from typing import *

from prisma.models import Departments, Employees, Jobs
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

from api.db import CSVModel
from api.lib import Faker

faker = Faker()


class EmployeeFaker(CSVModel):
    """Fake data generator"""

    name: str = Field(default_factory=faker.gen_name)
    datetime: str = Field(default_factory=faker.gen_datetime)


class JobCreate(CSVModel):
    """Job Create Model"""

    job: str = Field(...)


class DepartmentCreate(CSVModel):
    """Department Create Model"""

    department: str = Field(...)


class EmployeeCreate(CSVModel):
    """Employee Create Model"""

    name: str = Field(...)
    datetime: str = Field(...)
    job_id: int = Field(...)
    department_id: int = Field(...)
