from redis import Redis

from api.config import REDIS_URI

redis_connection = Redis.from_url(REDIS_URI)
