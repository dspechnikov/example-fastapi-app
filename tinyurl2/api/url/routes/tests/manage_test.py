from http import HTTPStatus

import pytest
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from tinyurl2.models.url import URL, URLManager

API_PREFIX = "/api/urls"


@pytest.mark.usefixtures("app_client", "db_session")
class TestURLManageRoutes:
    def test_create_short_url(self):
        target_url = "http://test.local"

        # follow_redirects=True to follow initial redirect by TestClient
        response = self.app_client.post(
            API_PREFIX, json={"target": target_url}, follow_redirects=True
        )

        assert response.status_code == HTTPStatus.OK
        url = self.db_session.scalars(select(URL)).one()
        assert url.target == target_url

    def test_delete_short_url(self):
        url = URLManager(self.db_session).create(
            URL.from_target_url("http://test.local")
        )

        response = self.app_client.delete(f"{API_PREFIX}/{url.id}")

        assert response.status_code == HTTPStatus.OK

        with pytest.raises(NoResultFound):
            self.db_session.scalars(select(URL).where(URL.id == url.id)).one()

    def test_change_target_url(self):
        new_url = "http://456"
        url = URLManager(self.db_session).create(URL.from_target_url("http://123"))

        response = self.app_client.patch(
            f"{API_PREFIX}/{url.id}", json={"target": new_url}
        )

        assert response.status_code == HTTPStatus.OK
        self.db_session.refresh(url)
        assert url.target == new_url

    def test_get_url_stats(self):
        url_manager = URLManager(self.db_session)
        url = url_manager.create(URL.from_target_url("http://123"))
        url_manager.click(url.id)

        response = self.app_client.get(f"{API_PREFIX}/{url.id}")

        assert response.status_code == HTTPStatus.OK
        assert response.json()["clicks"] == 1
