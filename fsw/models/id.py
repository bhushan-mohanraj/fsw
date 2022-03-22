from sqlalchemy import Column, types


class IDModelMixin:
    """
    Add an integer, primary key ID column to a model.
    """

    id = Column(
        types.Integer,
        primary_key=True,
    )
