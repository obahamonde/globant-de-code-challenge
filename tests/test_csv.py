import pytest
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from api.db import CSVModel


def test_valid_csv():
    models = CSVModel.from_csv("static/employees.csv")
    assert isinstance(models, list)
    for model in models:
        assert isinstance(model, BaseModel)
        assert isinstance(model.schema(), dict)
        assert isinstance(model.schema_json(), str) 

def test_not_csv():
    with pytest.raises(ValueError):
        models = CSVModel.from_csv("static/notcsv.xml")
        