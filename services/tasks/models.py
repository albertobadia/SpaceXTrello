import datetime
import enum
import typing
import uuid

from fastapi import status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field, ValidationError, model_validator


class TaskStatus(str, enum.Enum):
    PENDING = "PENDING"
    CREATED = "CREATED"
    ERROR = "ERROR"


class TaskCategory(str, enum.Enum):
    MAINTENANCE = "MAINTENANCE"
    RESEARCH = "RESEARCH"
    TEST = "TEST"


class TaskType(str, enum.Enum):
    ISSUE = "ISSUE"
    BUG = "BUG"
    TASK = "TASK"


class TaskCreate(BaseModel):
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
    id: uuid.UUID
    user: uuid.UUID
    received_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    trello_data: typing.Optional[dict] = None
    fail_count: int = 0


class TasksQuery(BaseModel):
    id: typing.Optional[uuid.UUID] = None
    user: typing.Optional[uuid.UUID] = None
    status: typing.Optional[TaskStatus] = None
