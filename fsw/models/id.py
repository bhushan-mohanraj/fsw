"""
A mixin that adds an ID column to a model.
"""

import sqlalchemy


class IDModelMixin:
    """
    A mixin that adds an integer, primary-key ID column to a model.
    """

    id = sqlalchemy.Column(
        sqlalchemy.types.Integer,
        primary_key=True,
    )
