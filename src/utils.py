import json
from random import choice

with open("..\\config.json", 'r', encoding="utf-8") as config_file:
    CONFIG = json.loads('\n'.join(config_file.readlines()))


def set_text(response, text):
    """
    :param response: json-response
    :param text: text to output
    :return: None
    """
    response['response']['text'] = text


def get_answer(field):
    return choice(CONFIG[field])
