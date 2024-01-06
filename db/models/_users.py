import sqlalchemy as sa
import sqlalchemy.orm as so

from sqlalchemy_utils import EmailType
from sqlalchemy.ext.hybrid import hybrid_property

from db.base import Base, DateFields, UUIDField


class UserModel(Base, UUIDField, DateFields):
    __tablename__ = "users"

    # PERSONAL INFO
    email: so.Mapped[EmailType] = so.mapped_column(
        EmailType(),  unique=True, nullable=False, index=True
    )
    first_name: so.Mapped[str] = so.mapped_column(
        sa.String(length=25), nullable=True
    )
    last_name: so.Mapped[str] = so.mapped_column(
        sa.String(length=25), nullable=True
    )

    # STATUSES
    is_active: so.Mapped[bool] = so.mapped_column(
        default=False, nullable=True
    )
    is_superuser: so.Mapped[bool] = so.mapped_column(
        default=False, nullable=True
    )

    # SECURITY
    hashed_password: so.Mapped[str] = so.mapped_column(
        sa.String(length=1024), nullable=True
    )

    @hybrid_property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".replace(
            "None", ""
        ).strip()

    @full_name.expression
    def full_name(cls):
        return sa.case(
            [
                (
                    sa.and_(cls.first_name.isnot(None), cls.last_name is None),
                    cls.first_name,
                ),
                (
                    sa.and_(cls.last_name.isnot(None), cls.first_name is None),
                    cls.last_name,
                ),
            ],
            else_=cls.first_name + " " + cls.last_name,
        ).label("full_name")
