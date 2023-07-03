from datetime import datetime
from random import choice, random
from typing import *

from names import get_full_name
from prisma.models import Departments, Jobs
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module


class FakerHelper(BaseModel):
    """Fake data generator"""

    jobs: List[str] = Field(default=[])
    deps: List[str] = Field(default=[])

    async def run(self) -> None:
        """Runs the Faker"""
        jobs = await Jobs.prisma().find_many()
        deps = await Departments.prisma().find_many()
        self.jobs = [job.job for job in jobs]
        self.deps = [dep.department for dep in deps]

    def gen_name(self) -> str:
        """Generates a random name"""
        return get_full_name()

    def gen_datetime(self) -> str:
        """Generates a random datetime in 2021"""
        dtime = self.gen_timestamp()
        return self.to_iso(dtime)

    def gen_timestamp(self) -> datetime:
        """Generates a random timestamp between 2021-01-01 and 2022-01-01"""
        start = datetime(year=2021, month=1, day=1)
        end = datetime(year=2021, month=12, day=31)
        random_date = start + (end - start) * random()
        return random_date

    def gen_job(self) -> str:
        """Generates a random job id"""
        return choice([job for job in self.jobs])

    def gen_department(self) -> str:
        """Generates a random department id"""
        return choice([dep for dep in self.deps])

    def from_iso(self, iso: str) -> datetime:
        """Converts an ISO datetime string to a datetime object"""
        return datetime.fromisoformat(iso)

    def to_iso(self, timestamp: datetime) -> str:
        """Converts a datetime object to an ISO datetime string"""
        return timestamp.isoformat()
