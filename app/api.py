import json
import logging

from app.read_config import config
import requests
import app.store as store
from app.Env import Env


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
    # TODO: not finished
    for_say = recipe_json['Steps'].replace(';', new_line * 2)
    text = f"""
     {recipe_json['Title']}
     {recipe_json['Description']}
     Ингредиенты
     {get_ingredients(recipe_json['IngSet'])}
     {new_line.join(
        [f'{b}: {a}' for a, b in zip(
            recipe_json['Energy'].split(";"),
            ['калорийность', 'белки', 'жиры', 'углеводы']
        )]
    )}
    Оценка: {recipe_json['Rating']}
     """
    if len(text) >= 1024:
        text = text[:1020] + "\n..."
    ''', [{
           "title": "Подробнее",
           "payload": {},
           "url": f"https://{Env.SITE}{recipe_json['Link']}",
           "hide": True
       }
       ]'''
    return text


def get_by_ingredients(good=[], bad=[]):
    """
    post request to search-server
    :param good: preferred ingredients
    :param bad: stop-list ingredients
    :return: None, if not found else
    """
    response = requests.get(Env.API_ADDRESS + "/find", json={
        "good": good,
        "bad": bad
    })
    if response.status_code != 200:
        return 'Ничего не нашлось', -1

    response = response.json()['response']
    return pretty_recipe(response), response['RecipeId']


def get_by_title(title, bad=[]):
    """
    :param title:
    :return:
    """
    response = requests.get(Env.API_ADDRESS + "/title", json={
        "title": title,
        "bad": bad
    })
    if response.status_code != 200:
        if response.text == "not found":
            return "Ничего не нашлось", -1
        return "Ничего не нашлось", -1
    response = response.json()['response']
    return pretty_recipe(response), response['RecipeId']


def send_rate(recipe_id, rate):
    response = requests.put(Env.API_ADDRESS + f"/rate/{recipe_id}/{rate}")
    if response.status_code != 200:
        logging.warning(f"WARN: Cant rate! {response.status_code} {response.text}")
        return


