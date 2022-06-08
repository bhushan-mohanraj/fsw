"""
Convert WTForms form classes to SQLAlchemy model classes.
"""

from sqlalchemy import inspect, types
from wtforms import fields, validators
from wtforms.fields import html5

# The output formats for the HTML date and time fields.
# WTForms provides inconsistent default values,
# so these values are passed when creating the fields.
TIME_FORMAT = "%H:%M"
DATE_FORMAT = "%Y-%m-%d"
DATETIME_LOCAL_FORMAT = "%Y-%m-%dT%H:%M"


# The WTForms field types corresponding to the SQLAlchemy column types.
_column_field_types = {
    types.String: fields.StringField,
    types.Integer: fields.IntegerField,
    types.DateTime: html5.DateTimeLocalField,
    types.Date: html5.DateField,
    types.Time: html5.TimeField,
    types.Boolean: fields.BooleanField,
    types.Enum: fields.SelectField,
}


def _column_field_type(column) -> type:
    """
    The field type for constructing a WTForms field from an SQLAlchemy column.
    """

    if type(column.type) in _column_field_types:
        return _column_field_types[type(column.type)]

    raise RuntimeError(
        f"{type(column.type)} columns cannot be converted to form fields."
    )


def _column_field_kwargs(column) -> dict:
    """
    Keyword arguments for constructing a WTForms field from an SQLAlchemy column.
    """

    # The label, description, and validators for the field.
    field_kwargs = {
        "label": column.name.replace("_", " ").title(),
        "description": column.doc if column.doc else "",
        "validators": [],
    }

    # The optional or input required validator.
    if column.nullable:
        field_kwargs["validators"] += [validators.Optional()]
    else:
        field_kwargs["validators"] += [validators.InputRequired()]

    # Keyword arguments for specific column types.
    if type(column.type) == types.String:
        field_kwargs["validators"] += [validators.Length(max=column.type.length)]
    elif type(column.type) == types.DateTime:
        field_kwargs["format"] = DATETIME_LOCAL_FORMAT
    elif type(column.type) == types.Date:
        field_kwargs["format"] = DATE_FORMAT
    elif type(column.type) == types.Time:
        field_kwargs["format"] = TIME_FORMAT
    elif type(column.type) == types.Enum:
        field_kwargs["choices"] = [
            (choice, choice.title()) for choice in column.type.enums
        ]

    return field_kwargs


class ModelFormMixin:
    """
    Add a class method to create WTForms form classes from SQLAlchemy model classes.
    """

    @classmethod
    def model_form(cls, model, fields: list[str]):
        """
        Create a WTForms form class from an SQLAlchemy model class.

        The `fields` parameter should specify the form fields to be created from the model.
        """

        class ModelForm(cls):
            """
            The form class created from the model.
            """

        columns = inspect(model).c

        for column in columns:
            name = column.name

            if name not in fields:
                continue

            field_type = _column_field_type(column)
            field_kwargs = _column_field_kwargs(column)

            setattr(ModelForm, name, field_type(**field_kwargs))

        return ModelForm
