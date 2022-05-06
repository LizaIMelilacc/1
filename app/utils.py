from random import choice
from pymorphy2 import MorphAnalyzer
from app.read_config import config
from app.Env import Env
import json

analyzer = MorphAnalyzer()


def to_normal_form(word):
    """Returns normal form (with PyMorphy2)"""
    return analyzer.parse(word)[0].normal_form


def set_text(response, text):
    """Set text to response"""
    response['response']['text'] = text


def set_tts(response, tts):
    response['response']['tts'] = tts


def set_buttons(response, buttons, hide=True):
    response['response']['buttons'] = [
        {
            "title": but,
            "hide": hide,
        } for but in buttons
    ]


def get_answer_option(field: str) -> str:
    """
    Choice random field option in config
    :param field: field in config with many options (greetings, for example)
    :return: random option of given field
    """
    return choice(config[field])


def get_ingredients(ing_set):
    """
    :param ing_set: IngSet field from json-response
    :return: text for output
    """
    answer = []
    counts = json.loads(ing_set["Counts"])
    max_length = 0
    for (title), (count) in zip(ing_set["Ingredients"], json.loads(ing_set["Counts"])):
        answer.append((title['Title'], counts[count], len(title["Title"])))
        max_length = max(max_length, len(title["Title"]))
    return '\n'.join([i[0] + Env.SEP * (max_length - i[2]) + Env.SEP * 5 + i[1] for i in answer])


def pretty_recipe(recipe_json):
    """
    :param recipe_json: JSON response from search API
    :return: user-readable text
    """
    new_line = '\n'
    text = f"""
     {recipe_json['Title']}
     {recipe_json['Description']}
     Ингредиенты
     {get_ingredients(recipe_json['IngSet'])}
     {new_line.join(
        [f'{b}: {a}' for a, b, c in zip(
            recipe_json['Energy'].split(";"),
            ['калорийность', 'белки', 'жиры', 'углеводы'],
            ['ККАЛ', 'ГРАММ', 'ГРАММ', 'ГРАММ']
        )]
    )}
    Оценка: {recipe_json['Rating']}
    Хотите оценить?
     """
    return text


def create_card(response, recipe_json):
    """
    Если успеем сделать фотокарточки то можно выдавать рецепт через Card, а не ткетс
    """
    body = pretty_recipe(recipe_json)
    tts = recipe_json['Steps'].replace(';', '\n\n')
    set_tts(response, tts)
    response['response']['card'] = {
        "type": "BigImage",
        "title": recipe_json['Title'],
        "description": body,
        "button": {
            "text": "Подробнее",
            "url": Env.SITE + recipe_json["Link"],
            "payload": {}
        }
    }
