"""
Convert SQLAlchemy model classes to WTForms form classes.
"""

import typing

import sqlalchemy
import wtforms

FormType = typing.Type[wtforms.Form]
FieldType = typing.Type[wtforms.Field]
FieldKwargs = dict[str, typing.Any]


class ColumnFieldConverter:
    """
    A converter from specific SQLAlchemy columns to WTForms fields.
    """

    def get_field_type(self, column: sqlalchemy.Column) -> FieldType:
        """
        Get the field type
        for the columns for which this converter is intended.
        """
        return wtforms.Field

    def get_field_kwargs(self, column: sqlalchemy.Column) -> FieldKwargs:
        """
        Get the keyword arguments to construct fields
        for the columns for which this converter is intended.
        """
        return {
            "label": column.name.replace("_", " ").title(),
            "description": getattr(column, "doc", None),
            "default": getattr(column, "default", None),
            "validators": [
                wtforms.validators.Optional()
                if column.nullable
                else wtforms.validators.InputRequired()
            ],
        }


class StringColumnFieldConverter(ColumnFieldConverter):
    def get_field_type(self, column: sqlalchemy.Column) -> FieldType:
        return wtforms.StringField

    def get_field_kwargs(self, column: sqlalchemy.Column) -> FieldKwargs:
        field_kwargs = super().get_field_kwargs(column)
        if column.type.length:
            field_kwargs["validators"].append(wtforms.validators.Length(max=column.type.length))

        return field_kwargs


class IntegerColumnFieldConverter(ColumnFieldConverter):
    def get_field_type(self, column: sqlalchemy.Column) -> FieldType:
        return wtforms.IntegerField


# NOTE: The WTForms `datetime-local` field
# has an incorrect format value that affects default-value rendering
# and does not support conversion from user timezones to UTC.
class DateTimeColumnFieldConverter(ColumnFieldConverter):
    def get_field_type(self, column: sqlalchemy.Column) -> FieldType:
        return wtforms.DateTimeLocalField


class DateColumnFieldConverter(ColumnFieldConverter):
    def get_field_type(self, column: sqlalchemy.Column) -> FieldType:
        return wtforms.DateField


class TimeColumnFieldConverter(ColumnFieldConverter):
    def get_field_type(self, column: sqlalchemy.Column) -> FieldType:
        return wtforms.TimeField


class BooleanColumnFieldConverter(ColumnFieldConverter):
    def get_field_type(self, column: sqlalchemy.Column) -> FieldType:
        return wtforms.BooleanField


class EnumColumnFieldConverter(ColumnFieldConverter):
    def get_field_type(self, column: sqlalchemy.Column) -> FieldType:
        return wtforms.SelectField

    def get_field_kwargs(self, column: sqlalchemy.Column) -> FieldKwargs:
        field_kwargs = super().get_field_kwargs(column)
        field_kwargs["choices"] = [(choice, choice.title()) for choice in column.type.enums]

        return field_kwargs


class ModelFormMixin:
    """
    A mixin that adds a `get_model_form` class method to the form class,
    which returns a class with fields matching the columns of the model.
    """

    converters: dict[typing.Type, ColumnFieldConverter] = {
        sqlalchemy.types.String: StringColumnFieldConverter(),
        sqlalchemy.types.Integer: IntegerColumnFieldConverter(),
        sqlalchemy.types.DateTime: DateTimeColumnFieldConverter(),
        sqlalchemy.types.Date: DateColumnFieldConverter(),
        sqlalchemy.types.Time: TimeColumnFieldConverter(),
        sqlalchemy.types.Boolean: BooleanColumnFieldConverter(),
        sqlalchemy.types.Enum: EnumColumnFieldConverter(),
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
                converter = cls.converters[type(column.type)]
            except KeyError:
                raise KeyError(
                    "No converter currently exists"
                    f" for SQLAlchemy columns of the type `{type(column.type)}`."
                )

            field_type = converter.get_field_type(column)
            field_kwargs = converter.get_field_kwargs(column)

            setattr(ModelForm, name, field_type(**field_kwargs))

        return ModelForm
