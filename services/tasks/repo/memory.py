from api.db.memory import InMemoryDB
from services.tasks.models import Task, TasksQuery, TaskUpdate
from services.tasks.repo.base import TasksRepo


class TasksMemoryRepo(TasksRepo):
    table = "tasks"

    def __init__(self, db: InMemoryDB) -> None:
        self.db = db

    def create(self, task: Task) -> Task:
        return Task(**self.db.create(table=self.table, data=task.model_dump()))

    def _filter_entry(self, entry: dict, query: TasksQuery) -> bool:
        if query.id and not query.id == entry.get("id"):
            print(query)
            return False

        if query.user and not query.user == entry.get("user"):
            return False

        if query.status and not query.status == entry.get("status"):
            return False

        return True

    def query(self, query: TasksQuery) -> list[Task]:
        return [
            Task(**entry)
            for entry in self.db.list(table=self.table)
            if self._filter_entry(entry=entry, query=query)
        ]

    def get(self, query: Task) -> Task:
        result = self.query(query=query)
        if not result:
            return None
        return result[0]

    def update(self, query: TasksQuery, data: TaskUpdate) -> list[Task]:
        for task in self.query(query=query):
            self.db.update(table=self.table, data=data.update_dict, id=task.id)
        return self.query(query=query)
