import os
import time

import redis

from app.AnswerTypes import AnswerTypes

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


def save_answer(user_id: str, answer: AnswerTypes):
    """
    Saving answer to redis
    :param user_id: user id
    :param answer: answer to user
    :return: None. Saving an answer to database for next operations
    """
    str_answer = str(answer)
    # TODO


def load_answer(user_id: str) -> str:
    """
    Loading answer from redis
    :param user_id: user id
    :return: previous answer to user
    """
    pass  # TODO


def save_recipe(user_id: str, recipe):
    """
    Saving recipe to redis
    :param user_id: user id
    :param recipe: recipe-json
    :return:
    """
    pass  # TODO


def load_recipe(user_id: str) -> dict:
    """
    Loading recipe from redis
    :param user_id: user id
    :return: recipe-json
    """
    pass  # TODO


if __name__ == "__main__":
    set_user_bad('foo', ['1', '4'])
    print(get_user_bad('foo'))
    print(store.ttl('foo'))
    time.sleep(10)
    print(get_user_bad('foo'))
