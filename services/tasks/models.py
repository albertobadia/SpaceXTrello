import datetime
import enum
import json
import typing
import uuid

from fastapi import status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field, model_validator


class TaskStatus(str, enum.Enum):
    """
    Enum for the status of a task.
    """

    PENDING = "PENDING"
    CREATED = "CREATED"
    ERROR = "ERROR"


class TaskCategory(str, enum.Enum):
    """
    Enum for the category of a task.
    """

    MAINTENANCE = "MAINTENANCE"
    RESEARCH = "RESEARCH"
    TEST = "TEST"


class TaskType(str, enum.Enum):
    """
    Enum for the type of a task.
    """

    ISSUE = "ISSUE"
    BUG = "BUG"
    TASK = "TASK"


class TaskCreate(BaseModel):
    """
    Model for creating a task. This model is used for validating the data sent to the API.

    Attributes:
        title (str): The title of the task.
        description (str): The description of the task.
        category (TaskCategory): The category of the task.
        type (TaskType): The type of the task.
    """

    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    category: typing.Optional[TaskCategory] = None
    type: TaskType = Field(default=TaskType.ISSUE)

    @model_validator(mode="before")
    def validate_entry(cls, data: dict):
        title = data.get("title")
        description = data.get("description")
        category = data.get("category")
        type = data.get("type")

        if type == TaskType.ISSUE and not all([title, description]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title and description are mandatory to create an issue",
            )

        if type == TaskType.BUG and description is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The description is mandatory to create a bug",
            )
        if type == TaskType.TASK and not all([title, category]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title and category are mandatory to create a task",
            )

        return data


class Task(TaskCreate):
    """
    Model for a task. This model is used for validating the data sent to the API.

    Attributes:
        id (uuid.UUID): The id of the task.
        user (uuid.UUID): The user id of the task.
        received_at (datetime.datetime): The date when the task was received.
        status (TaskStatus): The status of the task.
        trello_data (dict): The trello data of the task.
        fail_count (int): The fail count of the task.
        title (str): The title of the task.
        description (str): The description of the task.
        category (TaskCategory): The category of the task.
        type (TaskType): The type of the task.
    """

    id: uuid.UUID
    user: uuid.UUID
    received_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    trello_data: typing.Optional[dict] = None
    fail_count: int = 0


class TaskUpdate(BaseModel):
    """
    Model for updating a task. This model is used for validating the data sent to the API.

    Attributes:
        title (str): The title of the task.
        description (str): The description of the task.
        status (TaskStatus): The status of the task.
        trello_data (dict): The trello data of the task.
    """

    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    status: typing.Optional[TaskStatus] = None
    trello_data: typing.Optional[dict] = None

    @property
    def update_json(self):
        """
        Returns the update as a JSON object.
        """
        return {
            k: v for k, v in json.loads(self.model_dump_json()).items() if v is not None
        }


class TasksQuery(BaseModel):
    """
    Model for querying tasks. This model is used for validating the data sent to the API.

    Attributes:
        id (uuid.UUID): The id of the task.
        user (uuid.UUID): The user id of the task.
        status (TaskStatus): The status of the task.
    """

    id: typing.Optional[uuid.UUID] = None
    user: typing.Optional[uuid.UUID] = None
    status: typing.Optional[TaskStatus] = None

    @property
    def query_json(self):
        """
        Returns the query as a JSON object.
        """
        return {
            k: v for k, v in json.loads(self.model_dump_json()).items() if v is not None
        }
