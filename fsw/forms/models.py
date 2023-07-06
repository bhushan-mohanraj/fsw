"""
Convert SQLAlchemy model classes to WTForms form classes.
"""

import typing

import sqlalchemy
import wtforms

FormType = typing.Type[wtforms.Form]
FieldTypeAndKwargs = tuple[typing.Type[wtforms.Field], dict[str, typing.Any]]


class ModelFormMixin:
    """
    A mixin that adds a `get_model_form` class method to the form class,
    which returns a class with fields matching the columns of the model.
    """

    column_converters: dict[
        typing.Type, typing.Callable[[sqlalchemy.Column], FieldTypeAndKwargs]
    ] = {}

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
