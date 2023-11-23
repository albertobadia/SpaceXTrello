import typing
import uuid

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """
    Represents a user creation request.

    Attributes:
        username (str): The username of the user to be created.
        password (str): The password of the user to be created.
    """

    username: str
    password: str


class UserDB(UserCreate):
    """
    Represents a user in the database.

    Attributes:
        id (uuid.UUID): The unique identifier for the user.
        username (str): The username of the user to be created.
        password (str): The password of the user to be created.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    # This field is a flexible store to save data like trello user <-> local user relationship.
    external_data: typing.Optional[dict] = Field(default_factory=dict)


class UserRead(BaseModel):
    """
    Represents a user object with read-only fields.

    Attributes:
        id (uuid.UUID): The unique identifier for the user.
        username (str): The username of the user to be created.
    """

    id: uuid.UUID
    username: str
    external_data: dict


class UsersQuery(BaseModel):
    """
    Represents a query for retrieving users from the database.

    Attributes:
        id (Optional[uuid.UUID]): The ID of the user to retrieve.
        username (Optional[str]): The username of the user to retrieve.
    """

    id: typing.Optional[uuid.UUID] = None
    username: typing.Optional[str] = None


class UserUpdateModel(BaseModel):
    external_data: typing.Optional[dict] = None
