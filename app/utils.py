from random import choice
from re import split as re_split

from pymorphy2 import MorphAnalyzer

from app.read_config import config
from app.store import *

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


def get_title(cmd: str) -> str:
    """
    Getting title from command
    :param cmd: user command
    :return: title of recipe
    """
    return cmd # Примитивное получение названия блюда.


def get_ingredients(cmd: str) -> list:
    """
    Getting ingredients from command
    :param cmd: user command
    :return: list of ingredients
    """
    return re_split(', | и | а также ', cmd)


def get_answer_option(field: str) -> str:
    """
    Choice random field option in config
    :param field: field in config with many options (greetings, for example)
    :return: random option of given field
    """
    return choice(config[field])


def go_to_start(response, user_id):
    set_text(response, get_answer_option("greetings"))
    save_answer(user_id, AnswerTypes.START)
