from services.auth.service import AuthService
from services.users.models import UserCreate, UserDB, UserRead, UsersQuery, UserUpdate
from services.users.repo.base import UsersRepo


class UsersService:
    """
    Service class for managing user-related operations.
    """

    def __init__(self, repo: UsersRepo) -> None:
        self.repo = repo

    def create(self, user: UserCreate) -> UserRead:
        """
        Creates a new user with the given username and password.

        Args:
            user (UserCreate): The user data to create.

        Returns:
            UserRead: The created user data.
        """
        query = UsersQuery(username=user.username)
        if self.repo.query(query=query):
            raise ValueError("Username already taken.")

        user = UserDB(
            username=user.username,
            # hash before storing
            password=AuthService.hash_password(
                user.password,
            ),
        )
        user = self.repo.create(user).model_dump()
        return UserRead(**user)

    def get(self, query: UsersQuery) -> UserRead:
        """
        Retrieves a user from the repository based on the provided query.

        Args:
            query (UsersQuery): The query used to retrieve the user.

        Returns:
            UserRead: The user that matches the query, or None if no user is found.
        """
        user = self.repo.get(query=query)
        if user is None:
            return None
        return UserRead(**user.model_dump())

    def update(self, query: UsersQuery, data: UserUpdate) -> list[UserDB]:
        """
        Update users records in the database.

        Args:
            query (UsersQuery): The query used to filter users to update.
            data (UserUpdate): The data to be update on users.

        Returns:
            list[UserRead]: The updated users list.
        """
        return self.repo.update(query=query, data=data)

    def authenticate(self, username: str, password: str) -> UserRead | None:
        """
        Authenticates a user with the given username and password.

        Args:
            username (str): The username of the user to authenticate.
            password (str): The password of the user to authenticate.

        Returns:
            UserRead | None: The authenticated user, or None if authentication failed.
        """
        query = UsersQuery(username=username)
        user = self.repo.get(query=query)
        if not user:
            return None

        if not AuthService.verify_password(
            plain_password=password, hashed_password=user.password
        ):
            return None

        return UserRead(**user.model_dump())
