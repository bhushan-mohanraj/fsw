"""
A mixin that adds a method for saving a model instance.
"""

import sqlalchemy.orm


class SaveMixin:
    """
    A mixin that adds a method for saving a model instance.
    """

    # The SQLAlchemy database session.
    database_session: sqlalchemy.orm.scoped_session

    def save(self) -> None:
        """
        Commit the changes to the model instance to the database.
        """

        # TODO: Consider returning a boolean, and return `False` for errors.
        self.database_session.add(self)
        self.database_session.commit()
