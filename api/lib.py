from datetime import datetime
from random import choice

from names import get_full_name


class Faker:
    """Fake data generator"""

    def gen_name(self) -> str:
        """Generates a random name"""
        return get_full_name()

    def gen_datetime(self) -> str:
        """Generates a random datetime"""
        return datetime.astimezone(datetime.now()).isoformat()

    def gen_timestamp(self) -> datetime:
        """Generates a random timestamp"""
        start = datetime(2021, 1, 1, 0, 0, 0)
        end = datetime(2021, 12, 31, 23, 59, 59)
        return choice([start, end])


def to_timestamp(iso: str):
    """Converts an ISO datetime string to a timestamp"""
    return datetime.fromisoformat(iso).timestamp()
