from typing import Union

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
    target_url: schemas.URLCreate, db: orm.Session = Depends(db_session)
) -> URL:
    return URLManager(db).create(entity=URL.from_target_url(target_url.target))


@router.patch("/{url_id}", response_model=schemas.URL)
def change_target_url(
    url_id: str, target_url: schemas.URLCreate, db: orm.Session = Depends(db_session)
) -> Union[URL, JSONResponse]:
    try:
        url = URLManager(db).change_target(url_id, target_url.target)
    except NoResultFound:
        raise HTTPException(status_code=404)

    return url


@router.delete("/{url_id}")
def delete_short_url(url_id: str, db: orm.Session = Depends(db_session)) -> str:
    try:
        URLManager(db).delete_url_by_id(url_id)
    except NoResultFound:
        raise HTTPException(status_code=404)

    return ""


@router.get("/{url_id}", response_model=schemas.URL)
@router.get("/{url_id}/stats", response_model=schemas.URLStats)
def get_url(url_id: str, db: orm.Session = Depends(db_session)) -> URL:
    try:
        url = URLManager(db).get_by(url_id)
    except NoResultFound:
        raise HTTPException(status_code=404)

    return url
