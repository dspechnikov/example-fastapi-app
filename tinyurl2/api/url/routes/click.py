from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import orm
from sqlalchemy.exc import NoResultFound
from starlette.responses import RedirectResponse

from tinyurl2.database.session import db_session
from tinyurl2.models.url import URLManager

router = APIRouter(prefix="")


@router.get("/{url_id}", response_class=RedirectResponse, status_code=302)
def click_short_url(url_id: str, db: orm.Session = Depends(db_session)) -> str:
    try:
        return URLManager(db).click(url_id)
    except NoResultFound:
        raise HTTPException(status_code=404)
