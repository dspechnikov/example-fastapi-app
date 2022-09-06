from http import HTTPStatus

from tinyurl2.database.managers import EntityManager
from tinyurl2.models.url import URL


def test_click_short_url(app_client, db_session):
    target_url = "http://test.local"
    url = EntityManager(db_session).create(URL.from_target_url(target_url))

    # 1. allow_redirects=False to prevent request to target url,
    #    we just need to know the location is correct
    # 2. TestClient redirects short urls (i.e. /urls) to full URL with hostname,
    #    so use full URL to avoid that
    response = app_client.get(f"{app_client.base_url}/{url.id}", allow_redirects=False)

    assert response.status_code == HTTPStatus.FOUND
    assert response.headers["location"] == target_url
    db_session.refresh(url)
    assert url.clicks == 1
