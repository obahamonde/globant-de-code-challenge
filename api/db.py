from __future__ import annotations

import csv
import os
from typing import List, Type, TypeVar

from pydantic import BaseModel  # pylint: disable=no-name-in-module
from pydantic import create_model  # pylint: disable=no-name-in-module

T = TypeVar("T", bound=BaseModel)


class CSVModel(BaseModel):
    """CSV Format Model"""

    @classmethod
    def from_csv(cls: Type[T], path: str) -> List[T]:
        """Converts a CSV file to a list of Pydantic models"""
        if not path.endswith(".csv"):
            raise ValueError("File is not a CSV")
        if not os.path.isfile(path):
            raise FileNotFoundError("File does not exist")
        with open(path, "r", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
            data = list(reader)
        for row in data:
            for key, value in row.items():
                if value.isdigit():
                    row[key] = int(value)
                else:
                    try:
                        row[key] = float(value)
                    except ValueError:
                        pass
        model = create_model(cls.__name__, **data[0])  # type: ignore
        return [model(**row) for row in data]
