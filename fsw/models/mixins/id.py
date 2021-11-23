from sqlalchemy import types, Column


class IDMixin:
    """
    Add an integer, primary key ID column to a model.
    """

    id = Column(
        types.Integer,
        primary_key=True,
    )
