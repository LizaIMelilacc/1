import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_ADDRESS = os.getenv("API_ADDRESS")


def get_by_ingredients(good=[], bad=[]):
    """
    post request to search-server
    :param good: preferred ingredients
    :param bad: stop-list ingredients
    :return: message
    """
    response = requests.get(API_ADDRESS + "/find", json={
        "good": good,
        "bad": bad
    })
    print(response.text)


def get_by_title(title):
    """
    :param title:
    :return:
    """
    # TODO
    pass


if __name__ == "__main__":
    get_by_ingredients(["молоко"], [])
