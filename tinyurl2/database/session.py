from sqlalchemy import orm
from sqlalchemy.orm import sessionmaker
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from tinyurl2.database.base import db_engine

# expire_on_commit=False to prevent separate DB transactions
# for created object attribute lookup. without that we would need to assign
# each created object to separate variables to use them after commit,
# i.e. obj_id = obj.id or obj_not_in_session = obj
Session = sessionmaker(bind=db_engine, future=True, expire_on_commit=False)


class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request.state.db = Session()
        try:
            response = await call_next(request)
        finally:
            request.state.db.close()

        return response


def db_session(request: Request) -> orm.Session:
    assert isinstance(request.state.db, orm.Session)
    return request.state.db
