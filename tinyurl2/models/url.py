"""URL models and data management logic."""
import secrets
import typing
from typing import Any, ClassVar, Self

from sqlalchemy import BigInteger, CursorResult, delete, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import Session as SASession

from tinyurl2.database.base import BaseModel


class URL(BaseModel):
    """A short URL pointing to target URL."""

    __tablename__ = "url"

    # underscore to avoid shadowing builtin Python function
    id_: Mapped[str] = mapped_column(
        name="id",
        primary_key=True,
        default=lambda: secrets.token_hex(4),
    )
    target: Mapped[str] = mapped_column(nullable=False)
    _clicks: Mapped[int] = mapped_column(
        BigInteger(),
        name="clicks",
        default=0,
        nullable=False,
    )

    @property
    def clicks(self) -> int:
        """Return clicks count for the URL."""
        return self._clicks

    @classmethod
    def from_target_url(cls, target_url: str) -> Self:
        """Construct URL instance from target url."""
        return cls(
            target=target_url,
        )

    def track_click(self) -> None:
        """Increase click count when the URL is clicked."""
        self._clicks += 1


class URLManager:
    """URL data management logic."""

    model_cls: ClassVar[type[URL]] = URL

    def __init__(self, db_session: SASession) -> None:
        """Initialize manager attributes."""
        self.db = db_session

    def create(self, entity: URL) -> URL:
        """Create a URL in DB."""
        with self.db.begin():
            self.db.add(entity)

        return entity

    def get_by(self, field_value: Any, field_name: str = "id_") -> URL:
        """Get URLs from DB filtered by given fields."""
        return self.db.scalars(
            select(self.model_cls).where(
                getattr(self.model_cls, field_name) == field_value,
            ),
        ).one()

    def click(self, url_id: str) -> str:
        """Track click event in DB."""
        with self.db.begin():
            url = self.get_by(url_id)

            url.track_click()

        return url.target

    def change_target(self, url_id: str, new_target: str) -> URL:
        """Change target URL for given URL id."""
        with self.db.begin():
            url = self.get_by(url_id)

            url.target = new_target

        return url

    def delete_url_by_id(self, url_id: str) -> None:
        """Delete  URL with given URL id."""
        with self.db.begin():
            # need explicit cast, because mypy doesn't recognize CursorResult.
            # details at https://github.com/sqlalchemy/sqlalchemy/issues/9185
            delete_result = typing.cast(
                CursorResult[Any],
                self.db.execute(
                    delete(self.model_cls).where(self.model_cls.id_ == url_id),
                ),
            )

        if delete_result.rowcount == 0:
            raise NoResultFound
