import secrets

from sqlalchemy import Column, Integer, String

from tinyurl2.database.base import BaseModel
from tinyurl2.database.managers import EntityManager


class URL(BaseModel):
    __tablename__ = "url"

    id = Column(String, primary_key=True, default=lambda: secrets.token_hex(4))
    target = Column(String, nullable=False)
    _clicks = Column(Integer, name="clicks", default=0, nullable=False)

    @property
    def clicks(self):
        return self._clicks

    @classmethod
    def from_target_url(cls, target_url):
        return cls(
            target=target_url,
        )

    def track_click(self):
        self._clicks += 1


class URLManager(EntityManager):
    model_cls = URL

    def click(self, url_id):
        with self.db.begin():
            url = self.get_by(url_id)

            url.track_click()

        return url.target

    def change_target(self, url_id, new_target):
        with self.db.begin():
            url = self.get_by(url_id)

            url.target = new_target

        return url
