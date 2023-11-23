import unittest

from api.setup import users_service
from services.users.factory import get_user_create_data
from services.users.models import UsersQuery


class UsersServiceTestCase(unittest.TestCase):
    def test_create_user(self):
        user_data = get_user_create_data()
        user = users_service.create(user=user_data)
        self.assertEqual(user_data.username, user.username)

    def test_get_user(self):
        user_data = get_user_create_data()
        users_service.create(user=user_data)

        user_data = get_user_create_data()
        user = users_service.create(user=user_data)
        query = UsersQuery(username=user.username)
        self.assertEqual(
            user.username,
            users_service.get(query=query).username,
        )

    def test_authenticate(self):
        user_data = get_user_create_data()
        users_service.create(user=user_data)

        self.assertTrue(
            users_service.authenticate(
                username=user_data.username, password=user_data.password
            )
        )
        self.assertFalse(
            users_service.authenticate(username=user_data.username, password="error")
        )
