import json

from rethinkdb import RethinkDB

from api.db.rethinkdb import get_or_create_table
from services.tasks.models import Task, TasksQuery, TaskUpdate
from services.tasks.repo.base import TasksRepo


class RethinkDBTasksRepo(TasksRepo):
    """
    RethinkDB tasks repository.
    """

    table = "tasks"

    def __init__(self, db: RethinkDB):
        """
        Args:
            db (RethinkDB): The rethinkdb instance.
        """
        self.db = db

    def create(self, task: Task) -> Task:
        """
        Creates a new task with the given data and returns the created task.

        Args:
            task (Task): The data for the task to be created.
        """
        get_or_create_table(self.table).insert(json.loads(task.model_dump_json())).run(
            self.db
        )
        return task

    def query(self, query: TasksQuery) -> list[Task]:
        """
        Queries the repository for tasks that match the given query.

        Args:
            query (dict): The query to match.
        """

        return [
            Task(**entry)
            for entry in get_or_create_table(self.table)
            .filter(query.query_json)
            .run(self.db)
        ]

    def get(self, query: TasksQuery) -> Task:
        """
        Gets a task that matches the given query.

        Args:
            query (TasksQuery): The query to match.
        """
        return next(iter(self.query(query=query)))

    def update(self, query: TasksQuery, data: TaskUpdate) -> list[Task]:
        """
        Updates the tasks that match the given query with the given update.

        Args:
            query (dict): The query to match.
            update (dict): The update to apply.
        """

        get_or_create_table("tasks").filter(query.query_json).update(
            data.update_json
        ).run(self.db)
        return self.query(query=query)
