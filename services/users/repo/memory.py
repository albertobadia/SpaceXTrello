from api.db.memory import InMemoryDB
from services.users.models import UserDB, UsersQuery
from services.users.repo.base import UsersRepo


class UsersMemoryRepo(UsersRepo):
    def __init__(self, db: InMemoryDB) -> None:
        self.db = db

    def create(self, user: UserDB) -> UserDB:
        return UserDB(**self.db.create(table="users", data=user.model_dump()))

    def _filter_entry(self, entry: dict, query: UsersQuery) -> bool:
        if query.id and not query.id == entry.get["id"]:
            return False

        if query.username and not query.username == entry.get("username"):
            return False

        return True

    def query(self, query: UsersQuery) -> list[UserDB]:
        return [
            UserDB(**entry)
            for entry in self.db.list(table="users")
            if self._filter_entry(entry=entry, query=query)
        ]

    def get(self, query: UsersQuery) -> UserDB:
        result = self.query(query=query)
        if not result:
            return None
        return result[0]
