from __future__ import annotations

import csv
from typing import *

from pydantic import Field  # pylint: disable=no-name-in-module

from api.db import CSVModel
from api.lib import FakerHelper

faker = FakerHelper()


class EmployeeFaker(CSVModel):
    """Fake data generator"""

    name: str = Field(default_factory=faker.gen_name)
    datetime: str = Field(default_factory=faker.gen_datetime)
    job: str = Field(default_factory=faker.gen_job)
    department: str = Field(default_factory=faker.gen_department)

    @classmethod
    def to_csv(cls, path: str, data: List[EmployeeFaker]) -> None:
        """Converts a list of Pydantic models to a CSV file"""
        with open(
            f"static/employees-{path}.csv", "w", encoding="utf-8-sig"
        ) as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=data[0].dict().keys())
            writer.writeheader()
            for row in data:
                writer.writerow(row.dict())

    @classmethod
    def gen_batch(cls, batch_size: int) -> List[EmployeeFaker]:
        """Generates a batch of fake data"""
        return [EmployeeFaker() for _ in range(batch_size)]


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
    job: str = Field(...)
    department: str = Field(...)
