from rq import Queue

from api.db.redis import redis_connection
from api.db.rethinkdb import rethinkdb_connection
from services.tasks.repo.rethinkdb import RethinkDBTasksRepo
from services.tasks.service import TasksService
from services.trello.service import TrelloService
from services.users.repo.rethinkdb import RethinkDBUsersRepo
from services.users.service import UsersService

rq_queue = Queue(name="tasks", connection=redis_connection)


users_repo = RethinkDBUsersRepo(db=rethinkdb_connection)
users_service = UsersService(repo=users_repo)

trello_service = TrelloService(users_service=users_service)

tasks_repo = RethinkDBTasksRepo(db=rethinkdb_connection)
tasks_service = TasksService(
    repo=tasks_repo,
    users_service=users_service,
    trello_service=trello_service,
    queue=rq_queue,
)
