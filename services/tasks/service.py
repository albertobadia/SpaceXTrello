import uuid

from api.config import TRELLO_TOKEN_USER_DATA_KEY
from services.tasks.models import Task, TaskCreate, TasksQuery, TaskType
from services.tasks.repo.base import TasksRepo
from services.trello.service import TrelloService
from services.users.models import UserDB
from services.users.service import UsersService


class TasksService:
    """
    Service class for managing tasks.

    Args:
        repo (TasksRepo): Repository for managing notes data.
        trello_service (TrelloService): Service for getting and creating trello data.
    """

    def __init__(
        self,
        repo: TasksRepo,
        users_service: UsersService,
        trello_service: TrelloService,
    ):
        self.repo = repo
        self.users_service = users_service
        self.trello_service = trello_service

    def create(self, task: TaskCreate, user: UserDB) -> Task:
        """
        Creates a new task with the given data and returns the created task.

        Args:
            task (Task): The data for the task to be created.

        Returns:
            Task: The created task.
        """
        task_data = Task(**task.model_dump(), id=uuid.uuid4(), user=user.id)

        if task.type == TaskType.TASK:
            task_data.trello_data = self.trello_service.create_task(
                token=user.external_data.get(TRELLO_TOKEN_USER_DATA_KEY),
                title=task_data.title,
                category=task_data.category,
            )

        self.repo.create(task=task_data)
        return task_data

    def query(self, query: TasksQuery) -> list[Task]:
        """
        Queries the repository for tasks that match the given query.

        Args:
            query (Task): The query to match tasks against.

        Returns:
            list[Task]: A list of tasks that match the given query.
        """
        return self.repo.query(query=query)

    def get(self, query: TasksQuery) -> Task:
        """
        Retrieves a task from the repository based on the given query.

        Args:
            query (TasksQuery): The query used to retrieve the task.

        Returns:
            Task: The task retrieved from the repository.
        """
        return self.repo.get(query=query)
