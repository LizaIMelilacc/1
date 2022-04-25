import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_ADDRESS = os.getenv("API_ADDRESS")
SITE = os.getenv("SITE")


def pretty_recipe(recipe_json):
    """
    :param recipe_json: JSON response from search API
    :return: user-readable text
    """
    new_line = '\n'
    # TODO: not finished
    return \
        f"""
        {recipe_json['Title']}
        {recipe_json['Description']}
        {recipe_json['Steps'].replace(';', new_line * 2)}
        """


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


def get_by_title(title):
    """
    :param title:
    :return:
    """
    # TODO
    pass


if __name__ == "__main__":
    print(get_by_ingredients(["молоко", "яйца"], ["рис"]))
