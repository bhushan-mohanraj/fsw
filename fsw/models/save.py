"""
A mixin that adds a method for saving a model instance.
"""

from fsw.models.base import DatabaseSessionModelMixin


class SaveModelMixin(DatabaseSessionModelMixin):
    """
    A mixin that adds a method for saving a model instance.
    """

    def save(self) -> None:
        """
        Commit the changes to the model instance to the database.
        """

        self.database_session.add(self)
        self.database_session.commit()
