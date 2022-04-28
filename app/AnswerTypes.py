from enum import Enum


# Это список возможных нами ответов пользователю в общем виде
# Отсутствует приветствие, т.к. оно не обрабатывается функцией exec_command и напрямую связано с HELP
class AnswerTypes(Enum):
    START = 1 # Отправляем пользователю описание навыка
    SET_BAD_LIST = 2 # Просим пользователя задать список запрещенных продуктов
    SET_TYPE_OF_SEARCHING = 3 # Просим пользователя задать тип поиска (по ингредиентам или названию)
    SET_INGREDIENTS = 4 # Просим пользователя задать ингредиенты (ветка с игредиентами)
    SET_TITLE = 5 # Просим пользователя задать название (ветка с названием)
    RECIPE = 6 # Отправляем пользователю рецепт
    WILL_RATE = 7
    SET_RATE = 8 # Просим пользователя задать оценку (опционально)
    WILL_REPEAT = 9

    @staticmethod
    def from_string(string):
        string = string[12:]
        if string == "START":
            return AnswerTypes.START
        if string == "SET_BAD_LIST":
            return AnswerTypes.SET_BAD_LIST
        if string == "SET_TYPE_OF_SEARCHING":
            return AnswerTypes.SET_TYPE_OF_SEARCHING
        if string == "SET_INGREDIENTS":
            return AnswerTypes.SET_INGREDIENTS
        if string == "SET_TITLE":
            return AnswerTypes.SET_TITLE
        if string == "RECIPE":
            return AnswerTypes.RECIPE
        if string == "WILL_RATE":
            return AnswerTypes.WILL_RATE
        if string == "SET_RATE":
            return AnswerTypes.SET_RATE
        if string == "WILL_REPEAT":
            return AnswerTypes.WILL_REPEAT
