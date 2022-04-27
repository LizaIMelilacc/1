from pymorphy2 import MorphAnalyzer
from random import choice

from app.AnswerTypes import AnswerTypes
from app.store import *
from app.api import get_by_title, get_by_ingredients, send_rate


analyzer = MorphAnalyzer()


def to_normal_form(word):
    """
    :param word: any russian word
    :return: infinitive of this word
    """
    return analyzer.parse(word)[0].normal_form


def set_text(response, text):
    """
    :param response: json-response
    :param text: text to output
    :return: None
    """
    response['response']['text'] = text


def exec_command(response, cmd):
    """
    parse params and execute
    :param response: json-response
    :param cmd: command
    :return: None. change values in response
    """
    command = set([to_normal_form(word) for word in cmd.lower().split()])
    previous_answer = AnswerTypes.SET_INGREDIENTS
    # ↑ Тут нужно подгрузить прошлый отправленный юзеру текст и преобразовать его в формат Answers. TODO

    repeat_words = {"сначала", "заново", "перезапустить", "помощь"}
    # refusal_words = {"нет"}
    # agreement_words = {"да", "согласный", "хотеть"}
    # continuation_words = {"следующий", "шаг", "продолжить"}

    user_id = response["session"]["user_id"]
    bad_list = get_user_bad(user_id)
    if command <= repeat_words:
        set_text(response, get_answer_option("help"))
        save_answer(AnswerTypes.HELP)
    elif previous_answer == AnswerTypes.SET_BAD_LIST:
        bad_list = []  # Тут получим bad-list, обработав command. TODO
        set_user_bad(user_id, bad_list)
        set_text(response, "Ищем рецепт по названию или имеющимся ингредиентам?")
        save_answer(AnswerTypes.SET_TYPE_OF_SEARCHING)
    elif previous_answer == AnswerTypes.SET_TYPE_OF_SEARCHING:
        if {"ингредиент", "ингредиенты"} & command:
            set_text(response, get_answer_option("ingredients"))
            save_answer(AnswerTypes.SET_INGREDIENTS)
        elif {'название'} & command:
            set_text(response, get_answer_option("title"))
            save_answer(AnswerTypes.SET_TITLE)
        else:
            set_text(response, "Не поняла вас. Напишите, пожалуйста, как вы хотите искать рецепт: по названию блюда или ингредиентам?")
    elif previous_answer == AnswerTypes.SET_TITLE:
        title = "Шарлотка" # Тут получим title, обработав command. TODO
        recipe = get_by_title(title, bad_list) # Нужно получить id рецепта для дальнейшего его сохранения в бд
        set_text(response, recipe)
    elif previous_answer == AnswerTypes.SET_INGREDIENTS:
        ingredients = ["яблоко"] # Тут получим ingredients, обработав command. TODO
        recipe = get_by_ingredients(ingredients, bad_list)
        set_text(response, recipe)
    elif previous_answer == AnswerTypes.SET_RATE:
        rate = int(command.pop()) # Примитивное получение рейтинга. Работает, когда command - число
        send_rate(rate)
    # Не доделано


def get_answer_option(field: str):
    """
    :param field: field in config with many options (greetings, for example)
    :return: random option of given field
    """
    return choice(config[field])


def save_answer(answer: AnswerTypes):
    """
    :param answer: answer to user
    :return: None. Saving the answer to database for next operations
    """
    # TODO
    pass

