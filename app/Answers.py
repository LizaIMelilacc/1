from enum import Enum


# Отсутствует приветствие, т.к. оно не обрабатывается функцией exec_command
class Answers(Enum):
    HELP = 1
    SET_BAD_LIST = 2
    SET_INGREDIENTS = 3
    SET_TITLE = 4
    SET_RATE = 5

    @staticmethod
    def from_string(string):
        string = string[9:]
        if string == "HELP":
            return Answers.HELP
        if string == "SET_BAD_LIST":
            return Answers.SET_BAD_LIST
        if string == "SET_INGREDIENTS":
            return Answers.SET_INGREDIENTS
        if string == "SET_TITLE":
            return Answers.SET_TITLE
        if string == "SET_RATE":
            return Answers.SET_RATE
        return None
