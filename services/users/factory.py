from faker import Faker

from services.users.models import UserDB

faker = Faker()


def get_user_create_data() -> UserDB:
    """
    Returns a dictionary containing data to create a new user.

    Returns:
        UserDB: A UserDB object containing the user data.
    """
    data = dict(
        username=faker.simple_profile()["username"],
        password=faker.password(),
    )
    return UserDB(**data)
