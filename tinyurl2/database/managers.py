from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.exc import NoResultFound

from tinyurl2.database.base import BaseModel


class EntityManager:
    model_cls: Optional[type[BaseModel]] = None

    def __init__(self, db_session):
        self.db = db_session

    def create(self, entity: BaseModel):
        with self.db.begin():
            self.db.add(entity)

        return entity

    def get_by(self, field_value, field_name="id"):
        assert self.model_cls is not None, "model_cls must be set to use this lookup"

        return self.db.scalars(
            select(self.model_cls).where(
                getattr(self.model_cls, field_name) == field_value
            )
        ).one()

    def delete(self, entity_id):
        assert self.model_cls is not None, "model_cls must be set to use this lookup"

        with self.db.begin():
            rows_deleted = self.db.execute(
                delete(self.model_cls).where(self.model_cls.id == entity_id)
            ).rowcount

        if rows_deleted == 0:
            raise NoResultFound
