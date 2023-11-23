from pydantic import BaseModel, HttpUrl


class TrelloAuthURLResponse(BaseModel):
    url: HttpUrl


class TrelloUserTokenSet(BaseModel):
    token: str


class TrelloUserTokenSetResult(BaseModel):
    result: bool
