from datetime import datetime

import uuid6
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID


meta = sa.MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    },
)


class Base(DeclarativeBase):
    metadata = meta

    def __repr__(self) -> str:
        return "<{0.__class__.__name__}(uuid={0.uuid!r})>".format(self)

    def __str__(self) -> str:
        return self.name if hasattr(self, "name") else super().__str__()


class UUIDField:
    __abstract__ = True

    uuid: so.Mapped[uuid6.UUID] = so.mapped_column(
        UUID(as_uuid=True),
        default=uuid6.uuid7,
        server_default=sa.text("uuid_generate_v7()"),
        primary_key=True,
        unique=True,
    )


class DateFields:
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=False),
        nullable=False,
        default=datetime.utcnow,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=False),
        nullable=True,
        onupdate=datetime.utcnow,
        server_onupdate=sa.text("CURRENT_TIMESTAMP"),
    )