import redis
from app.AnswerTypes import AnswerTypes
from app.Env import Env

ex = Env.EX
port = Env.REDIS_PORT
ANSWER_ID = 1
BAD_LIST_ID = 0
CONNECTION_ERROR = False
try:
    store = redis.Redis(host="localhost", port=port, db=0)
except redis.exceptions.ConnectionError:
    CONNECTION_ERROR = True


def get_user_data(user_id: str) -> list:
    if CONNECTION_ERROR:
        return ['', '']
    data = store.get(user_id)
    if data is None:
        set_user_data(user_id, ['', ''])
        print("new")
        return ['', '']
    res = data.decode().split(';')
    res[BAD_LIST_ID] = res[BAD_LIST_ID].split(',')
    return res


def set_user_data(user_id: str, data: list):
    if CONNECTION_ERROR:
        return
    data[BAD_LIST_ID] = ','.join(data[BAD_LIST_ID])
    print("data to set = ", end='')
    print(';'.join(data))
    store.set(user_id, ';'.join(data), ex=ex)


def set_user_bad(user_id: str, bad: list):
    if CONNECTION_ERROR:
        return
    current_data = get_user_data(user_id)
    current_data[BAD_LIST_ID] = ','.join(bad)
    set_user_data(user_id, current_data)


def save_answer(user_id: str, answer: AnswerTypes):
    """
    Saving answer to redis
    :param user_id: user id
    :param answer: answer to user
    :return: None. Saving an answer to database for next operations
    """
    if CONNECTION_ERROR:
        return
    str_answer = str(answer)
    current_data = get_user_data(user_id)
    current_data[ANSWER_ID] = str_answer
    set_user_data(user_id, current_data)


def load_answer(user_id: str) -> str:
    """
    Loading answer from redis
    :param user_id: user id
    :return: previous answer to user
    """
    if CONNECTION_ERROR:
        return "START"
    return get_user_data(user_id)[ANSWER_ID]


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
