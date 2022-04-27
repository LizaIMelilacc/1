import os
import time
from app.read_config import config  # Нужен для чтения .env

import redis

ex = int(os.getenv("EX"))
port = int(os.getenv("REDIS_PORT"))
store = redis.Redis(host="localhost", port=port, db=0)


def get_user_bad(user_id: str) -> list:
    data = store.get(user_id)
    if data is None:
        set_user_bad(user_id, [])
        return []
    return data.decode().split(';')


def set_user_bad(user_id: str, bad: list):
    store.set(user_id, ';'.join(bad), ex=ex)


if __name__ == "__main__":
    set_user_bad('foo', ['1', '4'])
    print(get_user_bad('foo'))
    print(store.ttl('foo'))
    time.sleep(10)
    print(get_user_bad('foo'))
