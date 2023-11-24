from rethinkdb import r

from api.config import RETHINKDB_DB_NAME, RETHINKDB_URI

uri = f"{RETHINKDB_URI}/{RETHINKDB_DB_NAME}"

rethinkdb_connection = r.connect(url=uri)


def get_or_create_db(db_name: str):
    if db_name not in r.db_list().run(rethinkdb_connection):
        r.db_create(db_name).run(rethinkdb_connection)
    return r.db(db_name)


def get_or_create_table_for_db(db_name: str, table_name: str):
    get_or_create_db(db_name)
    if table_name not in r.table_list().run(rethinkdb_connection):
        r.table_create(table_name).run(rethinkdb_connection)
    return r.table(table_name)


def get_or_create_table(table_name: str):
    return get_or_create_table_for_db(RETHINKDB_DB_NAME, table_name)
