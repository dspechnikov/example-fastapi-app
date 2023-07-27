"""Entity schemas for URL API."""

from pydantic import BaseModel as BaseSchema
from pydantic import Field


class URL(BaseSchema):
    """A short URL pointing to some target URL."""

    # underscore to avoid shadowing builtin id function
    id_: str = Field(
        # use aliases so JSON wouldn't contain underscores for the client
        validation_alias="id",
        serialization_alias="id",
    )
    target: str
    clicks: int

    class Config:
        """A Pydantic model configuration."""

        orm_mode = True


class URLCreate(BaseSchema):
    """Request schema for URL creation."""

    target: str


class URLStats(BaseSchema):
    """Response schema for URL statistics view."""

    clicks: int
