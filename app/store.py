import redis
from app.AnswerTypes import AnswerTypes
from app.Env import Env

ex = Env.EX
port = Env.REDIS_PORT
store = redis.Redis(host="localhost", port=port, db=0)
ANSWER_ID = 1
BAD_LIST_ID = 0


def get_user_data(user_id: str) -> list:
    data = store.get(user_id)
    if data is None:
        set_user_data(user_id, ['', ''])
        print("new")
        return ['', '']
    res = data.decode().split(';')
    res[BAD_LIST_ID] = res[0].split(',')
    return res


def set_user_data(user_id: str, data: list):
    print(f"{data=}")
    data[BAD_LIST_ID] = ','.join(data[BAD_LIST_ID])
    store.set(user_id, ';'.join(data), ex=ex)


def save_answer(user_id: str, answer: AnswerTypes):
    """
    Saving answer to redis
    :param user_id: user id
    :param answer: answer to user
    :return: None. Saving an answer to database for next operations
    """
    str_answer = str(answer)
    current_data = get_user_data(user_id)
    print(current_data)
    current_data[ANSWER_ID] = str_answer
    set_user_data(user_id, current_data)


def load_answer(user_id: str) -> str:
    """
    Loading answer from redis
    :param user_id: user id
    :return: previous answer to user
    """
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
