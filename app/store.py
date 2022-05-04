from app.AnswerTypes import AnswerTypes


class UserData:
    def __init__(self, response):
        self.current_recipe_id = -1
        self.bad = []
        self.good = []
        self.dialog_point = AnswerTypes.WELCOME
        if 'session_state' in response:
            try:
                self.current_recipe_id = response['session_state']['current_recipe_id']
                self.bad = response['session_state']['bad']
                self.good = response['session_state']['good']
                self.dialog_point = response['session_state']['current_state']
            except KeyError:
                self.current_recipe_id = -1
                self.bad = []
                self.good = []
                self.dialog_point = AnswerTypes.WELCOME
        else:
            response['session_state'] = {}

    def commit(self, response):
        response['session_state']['current_recipe_id'] = self.current_recipe_id
        response['session_state']['bad'] = self.bad
        response['session_state']['good'] = self.good
        response['session_state']['current_state'] = self.dialog_point

    def __str__(self):
        return f"{self.dialog_point}, {self.current_recipe_id}, {self.bad}, {self.good}"
