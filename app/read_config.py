import json


def load_config():
    with open('config.json', 'r', encoding="utf-8") as config_file:
        CONFIG = json.loads('\n'.join(config_file.readlines()))
    return CONFIG
