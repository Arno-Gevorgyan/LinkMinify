import uuid6
import sqlalchemy as sa
import sqlalchemy.orm as so
from db.base import Base, DateFields, UUIDField

from db.models import UserModel


class ShortLinkModel(Base, UUIDField, DateFields):
    __tablename__ = "short_links"

    short_url: so.Mapped[str] = so.mapped_column(
        sa.String(length=25), index=True, unique=True,  nullable=False
    )
    full_url: so.Mapped[str] = so.mapped_column(
        sa.String(length=2000), index=True, unique=True, nullable=False
    )


class UserShortLinkModel(Base, UUIDField, DateFields):
    __tablename__ = "user_short_links"

    user_id: so.Mapped[uuid6.UUID] = so.mapped_column(sa.ForeignKey('users.uuid', ondelete='CASCADE'))
    user: so.Mapped[UserModel] = so.relationship('UserModel', uselist=False, backref=so.backref(
        'user_links', cascade="all, delete", lazy='selectin'))
    short_link_id: so.Mapped[uuid6.UUID] = so.mapped_column(sa.ForeignKey('short_links.uuid', ondelete='CASCADE'))
    short_link: so.Mapped[ShortLinkModel] = so.relationship('ShortLinkModel', uselist=False, backref=so.backref(
        'links', cascade="all, delete", lazy='selectin'))
