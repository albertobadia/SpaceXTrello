import abc

from services.tasks.models import Task, TasksQuery, TaskUpdate


class TasksRepo(abc.ABC):
    """Abstract base class for task repository."""

    @abc.abstractmethod
    def create(self, task: Task) -> Task:
        """
        Creates a new task in the database.

        Args:
            task (Task): The task to create.

        Returns:
            Task: The created task.
        """
        pass

    @abc.abstractmethod
    def query(self, query: TasksQuery) -> list[Task]:
        """
        Queries the database for tasks that match the given query.

        Args:
            query (TasksQuery): The query to match tasks against.

        Returns:
            list[Task]: A list of tasks that match the given query.
        """
        pass

    @abc.abstractmethod
    def get(self, query: TasksQuery) -> Task:
        """
        Retrieves a task from the database based on the provided query.

        Args:
            query (TasksQuery): The query used to retrieve the task.

        Returns:
            Task: The task retrieved from the database.
        """
        pass

    @abc.abstractmethod
    def update(self, query: TasksQuery, data: TaskUpdate) -> list[Task]:
        """
        Updates a task in the database based on the provided query.

        Args:
            query (TasksQuery): The query used to retrieve the task.
            update (TaskUpdate): The update to apply to the task.

        Returns:
            list[Task]: A list of tasks that were updated.
        """
        pass
