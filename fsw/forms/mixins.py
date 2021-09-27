import os

from flask import session

from wtforms import validators, fields
from wtforms.fields import html5
from wtforms.csrf.session import SessionCSRF

from sqlalchemy import inspect, types


class SessionCSRFMixin:
    """
    Add CSRF to forms using the Flask session.
    """

    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = os.urandom(32)
        csrf_context = session


# The default date format returned by the HTML5 datetime field.
DATETIME_LOCAL_FORMAT = "%Y-%m-%dT%H:%M"


class ModelMixin:
    """
    Add a classmethod to create WTForms form classes from SQLAlchemy model classes.
    """

    @classmethod
    def from_model(cls, model, exclude_names: list[str] = [], submit: bool = True):
        """
        Create a WTForms form class from an SQLAlchemy model class.

        Any excluded columns can be listed in the exclude_names list.

        A submit field is added to the form by default.
        """

        class ModelForm(cls):
            pass

        columns = inspect(model).c

        for column in columns:
            name = column.name

            # Skip any excluded column names and skip the ID column.
            if name in exclude_names or name == "id":
                continue

            # The field type, corresponding to the column type.
            field_type = None

            # Any keyword arguments required for constructing the field.
            field_kwargs = {
                "label": name.replace("_", " ").title(),
                "validators": [],
            }

            if column.doc:
                field_kwargs["description"] = column.doc

            # Determine the field type.
            if type(column.type) == types.Integer:
                field_type = fields.IntegerField

            elif type(column.type) == types.String:
                field_type = fields.StringField

                field_kwargs["validators"] += [
                    validators.Length(max=column.type.length)
                ]

            elif type(column.type) == types.Boolean:
                field_type = fields.BooleanField

            elif type(column.type) == types.Enum:
                field_type = fields.SelectField

                field_kwargs["choices"] = [
                    (choice, choice.title()) for choice in column.type.enums
                ]

            elif type(column.type) == types.DateTime:
                field_type = html5.DateTimeLocalField

                field_kwargs["format"] = DATETIME_LOCAL_FORMAT

            # Add the input required or optional validator.
            if not column.nullable:
                field_kwargs["validators"] += [validators.InputRequired()]
            else:
                field_kwargs["validators"] += [validators.Optional()]

            if field_type is None:
                raise RuntimeError(
                    "The column type {} "
                    "cannot currently be converted "
                    "to a form field.".format(type(column.type))
                )

            # Construct the field and add it to the form.
            setattr(
                ModelForm,
                name,
                field_type(**field_kwargs),
            )

        if submit:
            setattr(
                ModelForm,
                "submit",
                fields.SubmitField("Submit"),
            )

        return ModelForm
