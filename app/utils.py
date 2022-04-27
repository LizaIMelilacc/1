from pymorphy2 import MorphAnalyzer
from random import choice
from app.Answers import Answers


from app.read_config import load_config

config = load_config()
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
    previous_command = '' # Тут нужно подгрузить прошлую команду юзера

    repeat_words = {"сначала", "заново", "перезапустить", "помощь"}
    refusal_words = {"нет"}
    agreement_words = {"да", "согласный", "хотеть"}
    continuation_words = {"следующий", "шаг", "продолжить"}

    if command in repeat_words:
        set_text(response, get_answer_option("help"))


def get_answer_option(field):
    """
    :param field: field in config with many options (greetings, for example)
    :return: random option of given field
    """
    return choice(config[field])
