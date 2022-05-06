import json
import logging
import requests
from app.Env import Env
from app import utils


def get_by_ingredients(good=[], bad=[]):
    response = requests.get(Env.API_ADDRESS + "/find", json={
        "good": good,
        "bad": bad
    })
    if response.status_code != 200:
        return {}
    return response.json()['response']


def get_by_title(title, bad=[]):
    response = requests.get(Env.API_ADDRESS + "/title", json={
        "title": title,
        "bad": bad
    })
    if response.status_code != 200:
        if response.text == "not found":
            return {}
        return {}
    return response.json()['response']


def get_by_id(_id):
    response = requests.get(Env.API_ADDRESS + f"/id/{_id}")
    if response.status_code != 200:
        return {}
    return response.json()['response']


def show_recipe(response, recipe):
    print(recipe)
    if "RecipeId" in recipe:
        utils.set_text(response, utils.pretty_recipe(recipe))
        return
    utils.set_text(response, "Ничего не нашлось")


def send_rate(recipe_id, rate):
    response = requests.put(Env.API_ADDRESS + f"/rate/{recipe_id}/{rate}")
    if response.status_code != 200:
        logging.warning(f"WARN: Cant rate! {response.status_code} {response.text}")
        return
