"""
A mixin that adds an ID column to a model.
"""

import sqlalchemy.orm


class IDModelMixin:
    """
    A mixin that adds an integer, primary-key ID column to a model.
    """

    id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
