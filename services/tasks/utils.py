import random

from faker import Faker

from api.config import TRELLO_BOARD_NAME, TRELLO_TOKEN_USER_DATA_KEY
from services.tasks.models import Task, TasksQuery, TaskStatus, TaskType, TaskUpdate
from services.users.models import UserDB

faker = Faker()


def create_trello_task(task: Task, user: UserDB):
    """
    Create a task in trello. This is a blocking function, so it should be run in a separate thread.

    Args:
        task (TaskCreate): Task data.
        user (UserDB): User data.
    """

    # This import is here to avoid circular imports
    from api.setup import tasks_service

    list_name = "To Do"
    token = user.external_data.get(TRELLO_TOKEN_USER_DATA_KEY)
    members = []
    labels = []

    board = tasks_service.trello_service.get_or_create_board(
        token=token, name=TRELLO_BOARD_NAME
    )
    trello_list = tasks_service.trello_service.get_or_create_list(
        token=token, board_id=board["id"], name=list_name
    )

    if task.type == TaskType.TASK:
        label = tasks_service.trello_service.get_or_create_label(
            token=token, board_id=board["id"], name=task.category.value
        )
        labels = [label["id"]]

    if task.type == TaskType.BUG:
        task.title = f"bug-{faker.word()}-{str(random.randint(0, 99999)).zfill(5)}"
        label = tasks_service.trello_service.get_or_create_label(
            token=token, board_id=board["id"], name="BUG"
        )
        labels = [label["id"]]
        members = [
            random.choice(
                tasks_service.trello_service.get_board_members(
                    token=token, board_id=board["id"]
                )
            )["id"]
        ]

    task.trello_data = tasks_service.trello_service.create_card(
        token=token,
        list_id=trello_list["id"],
        name=task.title,
        description=task.description,
        labels=labels,
        members=members,
    )
    update_data = TaskUpdate(**task.model_dump() | dict(status=TaskStatus.CREATED))
    tasks_service.update(query=TasksQuery(id=task.id), data=update_data)
