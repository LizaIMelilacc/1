# Это список возможных нами ответов пользователю в общем виде
# Отсутствует приветствие, т.к. оно не обрабатывается функцией exec_command и напрямую связано с HELP
class AnswerTypes:
    WELCOME = 0  # К началу
    START = 10
    HELP = -1  # Отправляем пользователю описание навыка
    RESET = -2
    FIND_NAME = 1
    FIND_LIST = 2
    SEARCH = 3
    SET_RATE = 4
    SET_BAD = 5

    @staticmethod
    def from_string(string):
        return eval(string)
