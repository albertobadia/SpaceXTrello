import random
import uuid

from faker import Faker

from api.config import TRELLO_BOARD_NAME, TRELLO_TOKEN_USER_DATA_KEY
from services.tasks.models import Task, TaskCreate, TasksQuery, TaskType
from services.tasks.repo.base import TasksRepo
from services.trello.service import TrelloService
from services.users.models import UserDB
from services.users.service import UsersService

faker = Faker()


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
        list_name = "To Do"

        task = Task(**task.model_dump(), id=uuid.uuid4(), user=user.id)
        token = user.external_data.get(TRELLO_TOKEN_USER_DATA_KEY)

        board = self.trello_service.get_or_create_board(
            token=token, name=TRELLO_BOARD_NAME
        )
        trello_list = self.trello_service.get_or_create_list(
            token=token, board_id=board["id"], name=list_name
        )

        members = []
        labels = []

        if task.type == TaskType.TASK:
            label = self.trello_service.get_or_create_label(
                token=token, board_id=board["id"], name=task.category.value
            )
            labels = [label["id"]]

        if task.type == TaskType.BUG:
            task.title = f"bug-{faker.word()}-{str(random.randint(0, 99999)).zfill(5)}"
            label = self.trello_service.get_or_create_label(
                token=token, board_id=board["id"], name="BUG"
            )
            labels = [label["id"]]
            members = [
                random.choice(
                    self.trello_service.get_board_members(
                        token=token, board_id=board["id"]
                    )
                )["id"]
            ]

        task.trello_data = self.trello_service.create_card(
            token=token,
            list_id=trello_list["id"],
            name=task.title,
            description=task.description,
            labels=labels,
            members=members,
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
