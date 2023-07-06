"""
Convert SQLAlchemy model classes to WTForms form classes.
"""

import typing

import sqlalchemy
import wtforms

FormType = typing.Type[wtforms.Form]
FieldTypeAndKwargs = tuple[typing.Type[wtforms.Field], dict[str, typing.Any]]


def convert_column(column: sqlalchemy.Column) -> FieldTypeAndKwargs:
    """
    Convert a generic SQLAlchemy column to a WTForms field.
    """
    field_kwargs = {
        "label": column.name.replace("_", " ").title(),
        "description": getattr(column, "doc", None),
        "default": getattr(column, "default", None),
        "validators": [
            wtforms.validators.Optional()
            if column.nullable
            else wtforms.validators.InputRequired()
        ],
    }

    return wtforms.Field, field_kwargs


def convert_string_column(column: sqlalchemy.Column) -> FieldTypeAndKwargs:
    """
    Convert a `String` SQLAlchemy column to a WTForms field.
    """
    field_type = wtforms.StringField
    _, field_kwargs = convert_column(column)

    if column.type.length:
        field_kwargs["validators"].append(wtforms.validators.Length(max=column.type.length))

    return field_type, field_kwargs


def convert_integer_column(column: sqlalchemy.Column) -> FieldTypeAndKwargs:
    """
    Convert an `Integer` SQLAlchemy column to a WTForms field.
    """
    field_type = wtforms.IntegerField
    _, field_kwargs = convert_column(column)

    return field_type, field_kwargs


def convert_date_time_column(column: sqlalchemy.Column) -> FieldTypeAndKwargs:
    """
    Convert a `DateTime` SQLAlchemy column to a WTForms field.
    """
    field_type = wtforms.DateTimeLocalField
    _, field_kwargs = convert_column(column)

    return field_type, field_kwargs


def convert_date_column(column: sqlalchemy.Column) -> FieldTypeAndKwargs:
    """
    Convert a `Date` SQLAlchemy column to a WTForms field.
    """
    field_type = wtforms.DateField
    _, field_kwargs = convert_column(column)

    return field_type, field_kwargs


def convert_time_column(column: sqlalchemy.Column) -> FieldTypeAndKwargs:
    """
    Convert a `Time` SQLAlchemy column to a WTForms field.
    """
    field_type = wtforms.TimeField
    _, field_kwargs = convert_column(column)

    return field_type, field_kwargs


def convert_boolean_column(column: sqlalchemy.Column) -> FieldTypeAndKwargs:
    """
    Convert a `Boolean` SQLAlchemy column to a WTForms field.
    """
    field_type = wtforms.BooleanField
    _, field_kwargs = convert_column(column)

    return field_type, field_kwargs


def convert_enum_column(column: sqlalchemy.Column) -> FieldTypeAndKwargs:
    """
    Convert a `Enum` SQLAlchemy column to a WTForms field.
    """
    field_type = wtforms.SelectField
    _, field_kwargs = convert_column(column)

    field_kwargs["choices"] = [(choice, choice.title()) for choice in column.type.enums]

    return field_type, field_kwargs


class ModelFormMixin:
    """
    A mixin that adds a `get_model_form` class method to the form class,
    which returns a class with fields matching the columns of the model.
    """

    column_converters: dict[
        typing.Type, typing.Callable[[sqlalchemy.Column], FieldTypeAndKwargs]
    ] = {
        sqlalchemy.types.String: convert_string_column,
        sqlalchemy.types.Integer: convert_integer_column,
        sqlalchemy.types.DateTime: convert_date_time_column,
        sqlalchemy.types.Date: convert_date_column,
        sqlalchemy.types.Time: convert_time_column,
        sqlalchemy.types.Boolean: convert_boolean_column,
        sqlalchemy.types.Enum: convert_enum_column,
    }

    @classmethod
    def get_model_form(cls, model, names: list[str]) -> FormType:
        """
        Create a WTForms form from an SQLAlchemy model.
        """

        class ModelForm(cls):
            """
            The form class created from the model.
            """

        columns = sqlalchemy.inspect(model).columns
        name_to_column_map = {column.name: column for column in columns}

        for name in names:
            try:
                column = name_to_column_map[name]
            except KeyError:
                raise KeyError(
                    f"The submitted name `{name}`"
                    " does not match any column"
                    f" of the SQLAlchemy model `{model.__name__}`."
                )

            try:
                column_converter = cls.column_converters[type(column.type)]
            except KeyError:
                raise KeyError(
                    "No converter function exists"
                    f" for SQLAlchemy columns of the type `{type(column.type)}`."
                )

            field_type, field_kwargs = column_converter(column)
            setattr(ModelForm, name, field_type(**field_kwargs))

        return ModelForm
