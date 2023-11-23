import abc

from services.users.models import UserDB, UsersQuery, UserUpdateModel


class UsersRepo(abc.ABC):
    """Abstract base class for user repository."""

    @abc.abstractmethod
    def create(self, user: UserDB) -> UserDB:
        """
        Creates a new user in the database.

        Args:
            user (UserDB): The user to create.

        Returns:
            UserDB: The created user.
        """
        pass

    @abc.abstractmethod
    def query(self, query: UsersQuery) -> list[UserDB]:
        """
        Queries the database for users that match the given query.

        Args:
            query (UsersQuery): The query to match users against.

        Returns:
            list[UserDB]: A list of users that match the given query.
        """
        pass

    @abc.abstractmethod
    def get(self, query: UsersQuery) -> UserDB:
        """
        Retrieves a user from the database based on the provided query.

        Args:
            query (UsersQuery): The query used to retrieve the user.

        Returns:
            UserDB: The user retrieved from the database.
        """
        pass

    @abc.abstractmethod
    def update(self, query: UsersQuery, data: UserUpdateModel) -> UserDB:
        """
        Update some user data upserting every field on data.

        Args:
            query (UsersQuery): The query used to retrieve the users to update.

        Returns:
            UserDB: The updated version of the user in db
        """
        pass
