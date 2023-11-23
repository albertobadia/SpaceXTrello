import os

from dotenv import dotenv_values

config = {
    **dotenv_values(".env"),
    **os.environ,
}


SECRET_KEY = config.get("SECRET_KEY", "NOSECRET")
ALGORITHM = config.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


TRELLO_API_KEY = config.get("TRELLO_API_KEY")
TRELLO_ACCESS_TOKEN = config.get("TRELLO_ACCESS_TOKEN")
