from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from tinyurl2.settings import settings

db_engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    future=True,
)


class BaseModel(DeclarativeBase):
    pass
