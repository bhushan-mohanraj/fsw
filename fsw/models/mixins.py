from sqlalchemy import (
    Column,
    types,
)

from sqlalchemy.orm import (
    declared_attr,
)


class IDMixin:
    id = Column(
        types.Integer,
        primary_key=True,
    )


class NameMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__
