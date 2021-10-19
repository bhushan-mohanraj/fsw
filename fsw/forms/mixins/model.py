"""
Convert WTForms form classes to SQLAlchemy model classes.
"""

from wtforms import validators, fields
from wtforms.fields import html5

from sqlalchemy import inspect, types


# The output formats for the HTML time, date, and datetime-local fields.
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
        f"The {type(column.type)} column type cannot be converted to a form field."
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


class ModelMixin:
    """
    Add a class method to create WTForms form classes from SQLAlchemy model classes.
    """

    @classmethod
    def from_model(cls, model, exclude_names: list[str] = [], submit: bool = True):
        """
        Create a WTForms form class from an SQLAlchemy model class.

        Any excluded column names can be included in the "exclude_names" list.

        A submit field is added by default.
        """

        class ModelForm(cls):
            """
            The form class created from the model.
            """

        columns = inspect(model).c

        for column in columns:
            name = column.name

            if name in exclude_names or name == "id":
                continue

            field_type = _column_field_type(column)
            field_kwargs = _column_field_kwargs(column)

            setattr(ModelForm, name, field_type(**field_kwargs))

        if submit:
            setattr(ModelForm, "submit", fields.SubmitField("Submit"))

        return ModelForm