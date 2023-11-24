from unittest import TestCase

from pydantic import ValidationError

from api.setup import tasks_service, users_service
from services.tasks.models import (
    TaskCategory,
    TaskCreate,
    TasksQuery,
    TaskType,
    TaskUpdate,
)
from services.tasks.utils import create_trello_task
from services.users.factory import get_user_create_data
from tests.trello_mock import TrelloMockMixin


class TasksServiceTestCase(TestCase, TrelloMockMixin):
    def setUp(self) -> None:
        self.start_mocks()

    def test_create_issue_task(self):
        user = users_service.create(user=get_user_create_data())
        task = TaskCreate(
            title="Test task", description="Test description", type=TaskType.ISSUE.value
        )
        created_task = tasks_service.create(task=task, user=user)

        self.assertEqual(task.title, created_task.title)
        self.assertEqual(task.description, created_task.description)

    def test_create_bug_task(self):
        user = users_service.create(user=get_user_create_data())
        task = TaskCreate(description="Test description", type=TaskType.BUG.value)
        created_task = tasks_service.create(task=task, user=user)

        create_trello_task(created_task, user)

        self.assertTrue(created_task.title)
        self.assertEqual(task.description, created_task.description)

    def test_create_task(self):
        user = users_service.create(user=get_user_create_data())
        task = TaskCreate(
            title="Test title",
            category=TaskCategory.MAINTENANCE.value,
            type=TaskType.TASK.value,
        )
        created_task = tasks_service.create(task=task, user=user)

        self.assertEqual(task.title, created_task.title)
        self.assertEqual(task.category, created_task.category)

    def test_create_task_invalid_category(self):
        user = users_service.create(user=get_user_create_data())
        with self.assertRaises(ValidationError):
            task = TaskCreate(
                title="Test title",
                category="invalid",
                type=TaskType.TASK.value,
            )
            tasks_service.create(task=task, user=user)

    def test_create_task_invalid_type(self):
        user = users_service.create(user=get_user_create_data())
        with self.assertRaises(ValidationError):
            task = TaskCreate(
                title="Test title",
                category=TaskCategory.MAINTENANCE.value,
                type="invalid",
            )
            tasks_service.create(task=task, user=user)

    def test_update_task_invalid_status(self):
        user = users_service.create(user=get_user_create_data())
        task = TaskCreate(
            title="Test title",
            category=TaskCategory.MAINTENANCE.value,
            type=TaskType.TASK.value,
        )
        created_task = tasks_service.create(task=task, user=user)
        query = TasksQuery(id=created_task.id)

        with self.assertRaises(ValidationError):
            data = TaskUpdate(status="invalid")
            tasks_service.update(query=query, data=data)
