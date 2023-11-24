import uuid

from rq import Queue, Retry

from services.tasks.models import Task, TaskCreate, TasksQuery
from services.tasks.repo.base import TasksRepo
from services.tasks.utils import create_trello_task
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
        queue: Queue,
    ):
        self.repo = repo
        self.users_service = users_service
        self.trello_service = trello_service
        self.queue = queue

    def create(self, task: TaskCreate, user: UserDB) -> Task:
        """
        Creates a new task with the given data and returns the created task.

        Args:
            task (Task): The data for the task to be created.

        Returns:
            Task: The created task.
        """

        task = Task(**task.model_dump(), id=uuid.uuid4(), user=user.id)
        self.queue.enqueue(
            create_trello_task, task, user, retry=Retry(max=6, interval=30)
        )
        return self.repo.create(task=task)

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

    def update(self, query: TasksQuery, data: Task) -> list[Task]:
        """
        Updates a task in the repository based on the given query.

        Args:
            query (TasksQuery): The query used to retrieve the task.
            update (Task): The update to apply to the task.

        Returns:
            list[Task]: A list of tasks that were updated.
        """
        return self.repo.update(query=query, data=data)
