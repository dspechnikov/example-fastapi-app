"""FastAPI application configuration."""

from fastapi import FastAPI

from tinyurl2.api.url.routes.click import router as url_click_router
from tinyurl2.api.url.routes.manage import router as url_manage_router
from tinyurl2.database.session import DBSessionMiddleware

app = FastAPI()

app.add_middleware(DBSessionMiddleware)

for router in (
    url_click_router,
    url_manage_router,
):
    app.include_router(router)
