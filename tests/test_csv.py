from pydantic import BaseModel  # pylint: disable=no-name-in-module

from api.db import CSVModel


def test_from_csv():
    models = CSVModel.from_csv("static/hired_employees.csv")
    assert isinstance(models, list)
    for model in models:
        assert isinstance(model, BaseModel)
        assert isinstance(model.schema(), dict)
        assert isinstance(model.schema_json(), str)
