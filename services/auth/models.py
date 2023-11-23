from pydantic import BaseModel


class Token(BaseModel):
    """
    Represents a token result for login.
    """

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    The data inside token payload.
    """

    username: str
