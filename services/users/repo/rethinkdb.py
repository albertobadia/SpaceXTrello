import json

from rethinkdb import RethinkDB

from api.db.rethinkdb import get_or_create_table
from services.users.models import UserDB, UsersQuery, UserUpdate
from services.users.repo.base import UsersRepo


class RethinkDBUsersRepo(UsersRepo):
    table = "users"

    def __init__(self, db: RethinkDB):
        self.db = db

    def create(self, user: UserDB) -> UserDB:
        get_or_create_table(self.table).insert(json.loads(user.model_dump_json())).run(
            self.db
        )
        return user

    def query(self, query: UsersQuery) -> list[UserDB]:
        return [
            UserDB(**entry)
            for entry in get_or_create_table(self.table)
            .filter(query.query_json)
            .run(self.db)
        ]

    def get(self, query: UsersQuery) -> UserDB:
        return next(iter(self.query(query=query)))

    def update(self, query: UsersQuery, data: UserUpdate) -> list[UserDB]:
        get_or_create_table(self.table).filter(query.query_json).update(
            data.update_json, non_atomic=True
        ).run(self.db)
        return self.query(query=query)
