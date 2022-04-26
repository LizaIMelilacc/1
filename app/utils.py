from pymorphy2 import MorphAnalyzer
import app.api as api
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


def set_buttons(response, buttons):
    """
    :param response: json-response
    :param buttons: buttons
    :return: None
    """
    response['response']['buttons'] = buttons


def exec_command(response, cmd):
    """
    parse params and execute
    :param response: json-response
    :param cmd: command
    :return: None. change values in response
    """
    command = [to_normal_form(word) for word in cmd.lower().split()]
    text, buttons = api.get_by_ingredients(["молоко", "яйцо"], ["сливки"])
    set_text(response, text)
    set_buttons(response, buttons)
    print(response)
    # Здесь ожидается сравнение полученных слов со словами-ключами
