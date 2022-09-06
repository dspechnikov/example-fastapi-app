from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from tinyurl2.settings import settings

db_engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    future=True,
)

BaseModel = declarative_base()
