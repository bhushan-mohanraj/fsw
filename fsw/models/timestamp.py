"""
Mixins that add timestamp columns
that record when a model instance was created, last updated, or deleted.
"""

import datetime
import typing

import sqlalchemy.orm

from fsw.models.base import DatabaseSessionModelMixin


class CreateTimestampModelMixin:
    """
    A mixin that adds a `created_at` timestamp column,
    which records when the instance was created (first saved to the database).

    All times are stored in UTC.
    """

    created_at: sqlalchemy.orm.Mapped[datetime.datetime] = sqlalchemy.orm.mapped_column(
        default=datetime.datetime.utcnow,
    )


class UpdateTimestampModelMixin:
    """
    A mixin that adds a `updated_at` timestamp column,
    which records when the instance was last updated (saved to the database).

    All times are stored in UTC.
    """

    updated_at: sqlalchemy.orm.Mapped[datetime.datetime] = sqlalchemy.orm.mapped_column(
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )


class DeleteTimestampModelMixin(DatabaseSessionModelMixin):
    """
    A mixin that adds a `deleted_at` timestamp column and a `delete` method,
    The mixin emulates deletion by flagging the timestamp with the current time
    rather than permanently removing the model instance from the database.

    To check that a model instance is not deleted,
    use `model_instance.deleted_at is None`.

    To query the database for model instances that are not deleted,
    execute `sqlalchemy.select(Model).where(Model.deleted_at != None)`.

    All times are stored in UTC.
    """

    deleted_at: sqlalchemy.orm.Mapped[typing.Optional[datetime.datetime]]

    def delete(self) -> None:
        """
        Flag the `deleted_at` timestamp column with the current time
        to indicate that the model instance is deleted.
        """

        self.deleted_at = datetime.datetime.utcnow()
        self.database_session.commit()
