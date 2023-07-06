"""
Base classes for the model mixins.
"""

import sqlalchemy.orm


class DatabaseSessionModelMixin:
    """
    A base class for model mixins which require the database session.
    """

    database_session: sqlalchemy.orm.scoped_session
