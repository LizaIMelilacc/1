import json
import logging
import requests
from app.Env import Env
from app.utils import *


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
    return response, response['RecipeId']


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


def get_by_id(_id):
    """
    :param _id: recipe id
    :return: pretty recipe + ID
    """
    response = requests.get(Env.API_ADDRESS + f"/id/{_id}")
    if response.status_code != 200:
        return "Ошибка", -1
    response = response.json()['response']
    return pretty_recipe(response), response['RecipeId']


def send_rate(recipe_id, rate):
    response = requests.put(Env.API_ADDRESS + f"/rate/{recipe_id}/{rate}")
    if response.status_code != 200:
        logging.warning(f"WARN: Cant rate! {response.status_code} {response.text}")
        return
