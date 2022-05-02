import redis
from app.AnswerTypes import AnswerTypes
from app.Env import Env

ex = Env.EX
port = Env.REDIS_PORT
DIALOG_POINT_ID = 0
BAD_LIST_ID = 1
GOOD_LIST_ID = 2
CURRENT_RECIPE = 3
CONNECTION_ERROR = False
try:
    store = redis.Redis(host="localhost", port=port, db=0)
except redis.exceptions.ConnectionError:
    CONNECTION_ERROR = True


class UserData:
    def __init__(self, user_id):
        self.user_id = user_id
        self.current_recipe_id = -1
        self.bad = []
        self.good = []
        self.dialog_point = AnswerTypes.WELCOME
        self.load_from_store()

    def load_from_store(self) -> list:
        if CONNECTION_ERROR:
            return
        data = store.get(self.user_id)
        if data is None:
            self.commit()
            return
        data = data.decode().split(';')
        if len(data) < CURRENT_RECIPE + 1:
            return
        self.current_recipe_id = data[CURRENT_RECIPE]
        self.dialog_point = AnswerTypes.from_string(data[DIALOG_POINT_ID])
        self.good = data[GOOD_LIST_ID].split(',')
        self.bad = data[BAD_LIST_ID].split(',')

    def commit(self):
        store.set(
            self.user_id,
            f"{self.dialog_point};{','.join(self.bad)};{','.join(self.good)};{self.current_recipe_id}",
            ex=ex
        )
