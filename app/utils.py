from pymorphy2 import MorphAnalyzer
from random import choice

from app.AnswerTypes import AnswerTypes
from app.store import *
from app.api import get_by_title, get_by_ingredients, send_rate, pretty_recipe

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


def get_bad_list(cmd: str) -> list:
    """
    Getting bad-list from command
    :param cmd: user command
    :return: list of bad ingredients
    """
    pass  # TODO


def get_title(cmd: str) -> str:
    """
    Getting title from command.
    :param cmd: user command
    :return: title of recipe
    """
    pass  # TODO


def get_ingredients(cmd: str) -> list:
    """
    Getting ingredients from command.
    :param cmd: user command
    :return: list of ingredients
    """
    pass  # TODO


def get_answer_option(field: str):
    """
    Choice random field option in config.
    :param field: field in config with many options (greetings, for example)
    :return: random option of given field
    """
    return choice(config[field])
