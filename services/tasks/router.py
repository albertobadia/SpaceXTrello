import typing
import uuid

from fastapi import APIRouter, HTTPException, status

from api.setup import tasks_service
from services.auth.handlers import UserDependsType
from services.tasks.models import Task, TaskCreate, TasksQuery, TaskStatus

router = APIRouter(tags=["tasks"])


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=Task,
)
def create(task: TaskCreate, user: UserDependsType):
    """
    Creates a new task with the given data and returns the created task.

    Args:
        task (Task): The data for the task to be created.
        user (UserDependsType): The user that is creating the task.
    """
    return tasks_service.create(task=task, user=user)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[Task],
)
def query(
    user: UserDependsType,
    status: typing.Optional[TaskStatus] = None,
) -> list[Task]:
    """
    Queries the repository for tasks that match the given query.

    Args:
        user (UserDependsType): The user that is querying the tasks.
        status (TaskStatus): The status of the tasks to query.
    """
    query = TasksQuery(user=user.id, status=status)
    return tasks_service.query(query=query)


@router.get(
    path="/{id}/",
    status_code=status.HTTP_200_OK,
    response_model=Task,
)
def get(id: uuid.UUID, user: UserDependsType) -> Task:
    """
    Gets a task with the given id.

    Args:
        id (uuid.UUID): The id of the task to get.
        user (UserDependsType): The user that is getting the task.
    """
    query = TasksQuery(id=id, user=user.id)

    tasks = tasks_service.query(query=query)
    if tasks:
        return tasks[0]
    raise HTTPException(status_code=404)
