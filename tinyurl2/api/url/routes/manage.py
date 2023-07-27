"""Request-response logic for short URL management."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import orm
from sqlalchemy.exc import NoResultFound
from starlette.responses import JSONResponse

from tinyurl2.api.url import schemas
from tinyurl2.database.session import db_session
from tinyurl2.models.url import URL, URLManager

router: APIRouter = APIRouter(
    prefix="/api/urls",
)


@router.post("", response_model=schemas.URL)
def create_short_url(
    target_url: schemas.URLCreate,
    db: orm.Session = Depends(db_session),
) -> URL:
    """
    Create short URL in DB.

    Used when user needs a new short URL.
    """
    return URLManager(db).create(entity=URL.from_target_url(target_url.target))


@router.patch("/{url_id}", response_model=schemas.URL)
def change_target_url(
    url_id: str,
    target_url: schemas.URLCreate,
    db: orm.Session = Depends(db_session),
) -> URL | JSONResponse:
    """
    Change short URL in DB.

    Used when a user needs to keep old short URL but change its target.
    """
    try:
        url = URLManager(db).change_target(url_id, target_url.target)
    except NoResultFound as exc:
        raise HTTPException(status_code=404) from exc

    return url


@router.delete("/{url_id}")
def delete_short_url(url_id: str, db: orm.Session = Depends(db_session)) -> str:
    """
    Delete short URL in DB.

    Used to free space in DB when URL is not needed anymore.
    """
    try:
        URLManager(db).delete_url_by_id(url_id)
    except NoResultFound as exc:
        raise HTTPException(status_code=404) from exc

    return ""


@router.get("/{url_id}", response_model=schemas.URL)
@router.get("/{url_id}/stats", response_model=schemas.URLStats)
def get_url(url_id: str, db: orm.Session = Depends(db_session)) -> URL:
    """
    Get short URL from DB.

    Useful for viewing various URL attributes.
    """
    try:
        url = URLManager(db).get_by(url_id)
    except NoResultFound as exc:
        raise HTTPException(status_code=404) from exc

    return url
