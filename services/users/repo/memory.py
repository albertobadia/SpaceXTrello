from api.db.memory import InMemoryDB
from services.users.models import UserDB, UsersQuery, UserUpdate
from services.users.repo.base import UsersRepo


class UsersMemoryRepo(UsersRepo):
    table = "users"

    def __init__(self, db: InMemoryDB) -> None:
        self.db = db

    def create(self, user: UserDB) -> UserDB:
        return UserDB(**self.db.create(table=self.table, data=user.model_dump()))

    def _filter_entry(self, entry: dict, query: UsersQuery) -> bool:
        if query.id and not query.id == entry.get("id"):
            return False

        if query.username and not query.username == entry.get("username"):
            return False

        return True

    def query(self, query: UsersQuery) -> list[UserDB]:
        return [
            UserDB(**entry)
            for entry in self.db.list(table=self.table)
            if self._filter_entry(entry=entry, query=query)
        ]

    def get(self, query: UsersQuery) -> UserDB:
        result = self.query(query=query)
        if not result:
            return None
        return result[0]

    def update(self, query: UsersQuery, data: UserUpdate) -> list[UserDB]:
        users = self.query(query=query)
        for user in users:
            self.db.update(table=self.table, id=user.id, data=data.update_dict)
        return self.query(query=query)
