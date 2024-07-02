from django import forms

import pytest

from hope_flex_fields.importers import validate_json
from hope_flex_fields.models import Fieldset


@pytest.fixture
def config(db):
    from hope_flex_fields.models import FieldDefinition, Fieldset, FieldsetField

    fd1 = FieldDefinition.objects.create(
        name="IntField", field_type=forms.IntegerField, attrs={"min_value": 1}
    )
    fd2 = FieldDefinition.objects.create(
        name="FloatField",
        field_type=forms.FloatField,
        attrs={"min_value": 1},
        validation="""if (value % 2 == 0) {result="Insert an odd number"}""",
    )
    fs = Fieldset.objects.create(name="Fieldset")

    FieldsetField.objects.create(name="int", field=fd1, fieldset=fs)
    FieldsetField.objects.create(name="float", field=fd2, fieldset=fs)
    data = [
        {"int": 1, "float": 2.0},
        {"int": 2, "float": 2.2},
        {"int": -3, "float": 2.1},
    ]
    return {"fs": fs, "data": data}


def test_validate_json(config):
    fs: Fieldset = config["fs"]
    result = validate_json(config["data"], fs.name)
    assert result == [
        {"float": ["Insert an odd number"]},
        "Ok",
        {"int": ["Ensure this value is greater than or equal to 1."]},
    ]
