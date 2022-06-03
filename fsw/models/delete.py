"""
A mixin for deleting model instances from the database.
"""

from fsw.models.base import DatabaseSessionModelMixin


# TODO: Determine the conventional term for "hard delete,"
# and consider replacing "hard delete" with "delete."
class HardDeleteModelMixin(DatabaseSessionModelMixin):
    """
    A mixin that adds a `hard_delete` method,
    which hard-deletes a model instance from the database.

    This mixin permanently deletes the data of the model instance.
    Consider using `DeleteTimestampModelMixin` instead, which emulates deletion
    by flagging a `deleted_at` timestamp column on the model instance.
    """

    def hard_delete(self) -> None:
        """
        Hard-delete the model instance from the database.
        """

        self.database_session.delete(self)
        self.database_session.commit()
