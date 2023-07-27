"""Base sqlalchemy entities."""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from tinyurl2.settings import settings

db_engine = create_engine(
    url=settings.database_url,
)


class BaseModel(DeclarativeBase):
    """Base sqlalchemy model."""
