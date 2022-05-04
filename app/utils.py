from random import choice
from pymorphy2 import MorphAnalyzer
from app.read_config import config

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


def set_tts(response, tts):
    response['response']['tts'] = tts


def get_answer_option(field: str) -> str:
    """
    Choice random field option in config
    :param field: field in config with many options (greetings, for example)
    :return: random option of given field
    """
    return choice(config[field])
