import app.api as api
from app.utils import *
from app.AnswerTypes import *
from app.kewords import Keywords


def contain(phrase: set, phrase_type: set) -> bool:
    return len(phrase.intersection(phrase_type)) != 0


def exec_command(response, cmd, test_user_data):
    print('exec command')
    print('Command: ' + cmd)
    """
    parse params and execute
    :param response: json-response
    :param cmd: command
    :return: None. change values in response
    """
    command = [to_normal_form(word) for word in cmd.lower().split()]
    command_set = set(command)
    print('Command set: ' + str(command_set))

    # continuation_words = {"следующий", "шаг", "продолжить"}

    user_id = response["session"]['user']["user_id"]
    print('User id: ' + user_id)
    user_data = test_user_data
    print(user_data.dialog_point)
    if cmd in Keywords.HELP:
        set_text(response, get_answer_option("help"))
        user_data.dialog_point = AnswerTypes.START
        user_data.commit()
        return
    if user_data.dialog_point == AnswerTypes.WELCOME:
        print("Point: WELCOME")
        user_data.bad = []  # При перезапуске отменяем стоп-лист
        set_text(response, get_answer_option("type_of_searching"))
        user_data.dialog_point = AnswerTypes.START
        user_data.commit()  # Сохраняем все изменения
        return
    elif user_data.dialog_point == AnswerTypes.START:
        print("Point: START")
        if contain(command_set, Keywords.TITLE_SEARCH):
            user_data.dialog_point = AnswerTypes.FIND_NAME
            set_text(response, get_answer_option('title'))
        elif contain(command_set, Keywords.LIST_SEARCH):
            user_data.dialog_point = AnswerTypes.FIND_LIST
            set_text(response, get_answer_option('ingredients'))
        else:
            set_text(response, get_answer_option("not_understand"))
    elif user_data.dialog_point == AnswerTypes.SET_BAD:
        print("Point: SET_BAD")
        if contain({cmd}, Keywords.STOP_WORD):
            user_data.dialog_point = AnswerTypes.WELCOME  # Добавить кнопки - оценить, повторить и в начало
        else:
            user_data.bad.append(cmd.lower())
    elif user_data.dialog_point == AnswerTypes.FIND_LIST:
        print("Point: FIND_LIST")
        if contain({cmd}, Keywords.STOP_WORD):
            answer, id = api.get_by_ingredients(user_data.good, user_data.bad)
            set_text(response, answer)
            user_data.dialog_point = AnswerTypes.SEARCH  # Добавить кнопки - оценить, повторить и в начало
            user_data.current_recipe_id = id
        else:
            user_data.good.append(cmd.lower())
    elif user_data.dialog_point == AnswerTypes.FIND_NAME:
        print("Point: FIND_NAME")
        print(api.get_by_title(cmd.lower(), user_data.bad))
        answer, id = api.get_by_title(cmd, user_data.bad)
        set_text(response, answer)
        user_data.current_recipe_id = id
        user_data.dialog_point = AnswerTypes.SEARCH
    elif user_data.dialog_point == AnswerTypes.SEARCH:
        print("Point: SEARCH")
        if contain({cmd}, Keywords.REPEAT):
            set_text(response, "")  # TODO: Сделать ручку
        elif contain({cmd}, Keywords.RATE):
            user_data.dialog_point = AnswerTypes.SET_RATE  # Добавить кнопки 1 2 3 4 5
            set_text(response, get_answer_option('rate'))
        else:
            set_text(response, get_answer_option('not_understand'))
    elif user_data.dialog_point == AnswerTypes.SET_RATE:
        print("Point: SET_RATE")
        set_text(response, get_answer_option('will_repeat'))
    user_data.commit()  # Сохраняем все изменения
