import os

from dotenv import dotenv_values

config = {
    **dotenv_values(".env"),
    **os.environ,
}

TESTING = bool(config.get("TESTING", False))

SECRET_KEY = config.get("SECRET_KEY", "NOSECRET")
ALGORITHM = config.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


TRELLO_TOKEN_USER_DATA_KEY = "trello_access_token"
TRELLO_API_KEY = config.get("TRELLO_API_KEY")
TRELLO_BOARD_NAME = config.get("TRELLO_BOARD_NAME", "SpaceXTrello")
TRELLO_TOKEN_EXPIRATION = config.get("TRELLO_TOKEN_EXPIRATION", "1day")
TRELLO_TOKEN_NAME = config.get("TRELLO_TOKEN_NAME", "SpaceXTrelloToken")

REDIS_URI = config.get("REDIS_URI", "redis://redis/")

RETHINKDB_DB_NAME = config.get("RETHINKDB_DB", "test")
RETHINKDB_URI = config.get("RETHINKDB_URI", "rethinkdb://rethinkdb:28015")
