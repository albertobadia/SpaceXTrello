from pydantic import BaseModel, HttpUrl


class TrelloAuthURLResponse(BaseModel):
    """
    Response model for the Trello auth URL
    """

    url: HttpUrl


class TrelloUserTokenSet(BaseModel):
    """
    Request model for setting the Trello user token
    """

    token: str


class TrelloUserTokenSetResult(BaseModel):
    """
    Response model for setting the Trello user token
    """

    result: bool
