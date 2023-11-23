from api.db.memory import InMemoryDB
from services.tasks.repo.memory import TasksMemoryRepo
from services.tasks.service import TasksService
from services.trello.service import TrelloService
from services.users.repo.memory import UsersMemoryRepo
from services.users.service import UsersService

db = InMemoryDB()

users_repo = UsersMemoryRepo(db=db)
users_service = UsersService(repo=users_repo)

trello_service = TrelloService()

tasks_repo = TasksMemoryRepo(db=db)
tasks_service = TasksService(repo=tasks_repo, trello_service=trello_service)
