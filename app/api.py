import json
from app.read_config import config
import requests
from dotenv import load_dotenv
from app.store import *

load_dotenv()
API_ADDRESS = os.getenv("API_ADDRESS")
SITE = os.getenv("SITE")
SEP = os.getenv("SEP")


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
    return '\n'.join([i[0] + SEP * (max_length - i[2]) + SEP * 5 + i[1] for i in answer])


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
     """
    if len(text) >= 1024:
        text = text[:1020] + "\n..."
    return text, [{
        "title": "Подробнее",
        "payload": {},
        "url": f"https://{SITE}{recipe_json['Link']}",
        "hide": True
    }
    ]


def get_by_ingredients(good=[], bad=[]):
    """
    post request to search-server
    :param good: preferred ingredients
    :param bad: stop-list ingredients
    :return: None, if not found else
    """
    response = requests.get(API_ADDRESS + "/find", json={
        "good": good,
        "bad": bad
    })
    if response.status_code != 200:
        return None

    return pretty_recipe(response.json()['response'])


def get_by_title(title, bad=[]):
    """
    :param title:
    :return:
    """
    response = requests.get(API_ADDRESS + "/title", json={
        "title": title,
        "bad": bad
    })
    if response.status_code != 200:
        if response.text == "not found":
            return "Ничего не нашлось"
        return None
    return pretty_recipe(response.json()['response'])


def send_rate(rate):
    # TODO
    pass


if __name__ == "__main__":
    set_user_bad('foo', ['1', '4'])
    print(get_user_bad('foo'))
    print(store.ttl('foo'))
    time.sleep(10)
    print(get_user_bad('foo'))

    print(get_by_ingredients(["молоко", "яйца"], ["рис"]))
