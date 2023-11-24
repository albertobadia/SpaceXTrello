from rq import Queue

from api.db.memory import InMemoryDB
from api.db.redis import redis_connection
from services.tasks.repo.memory import TasksMemoryRepo
from services.tasks.service import TasksService
from services.trello.service import TrelloService
from services.users.repo.memory import UsersMemoryRepo
from services.users.service import UsersService

db = InMemoryDB()
rq_queue = Queue(name="tasks", connection=redis_connection)


users_repo = UsersMemoryRepo(db=db)
users_service = UsersService(repo=users_repo)

trello_service = TrelloService(users_service=users_service)

tasks_repo = TasksMemoryRepo(db=db)
tasks_service = TasksService(
    repo=tasks_repo,
    users_service=users_service,
    trello_service=trello_service,
    queue=rq_queue,
)
