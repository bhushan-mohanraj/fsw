from sqlalchemy import (
    Column,
    types,
)

from sqlalchemy.orm import (
    declared_attr,
)


class IDMixin:
    """
    Add an integer, primary key ID column to a model.
    """

    id = Column(
        types.Integer,
        primary_key=True,
    )


class NameMixin:
    """
    Set the table name of the model to the model class name.
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__
