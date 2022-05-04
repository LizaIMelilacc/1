from app.AnswerTypes import AnswerTypes
from pprint import *


class UserData:
    def __init__(self, response):
        self.current_recipe_id = -1
        self.bad = []
        self.good = []
        self.dialog_point = AnswerTypes.WELCOME
        pprint(response)
        if 'session_state' in response:
            try:
                self.current_recipe_id = response['session_state']['recipe']
                self.bad = response['session_state']['bad']
                self.good = response['session_state']['good']
                self.dialog_point = response['session_state']['point']
            except KeyError:
                self.current_recipe_id = -1
                self.bad = []
                self.good = []
                self.dialog_point = AnswerTypes.WELCOME
        else:
            response['session_state'] = {}

    def commit(self, response):
        response['session_state']['recipe'] = self.current_recipe_id
        response['session_state']['bad'] = self.bad
        response['session_state']['good'] = self.good
        response['session_state']['point'] = self.dialog_point

    def __str__(self):
        return f"{self.dialog_point}, {self.current_recipe_id}, {self.bad}, {self.good}"
