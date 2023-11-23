from pydantic import BaseModel


class TrelloData(BaseModel):
    data: dict = None
