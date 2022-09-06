from pydantic import BaseModel as BaseSchema


class URL(BaseSchema):
    id: str
    target: str
    clicks: int

    class Config:
        orm_mode = True


class URLCreate(BaseSchema):
    target: str


class URLStats(BaseSchema):
    clicks: int
