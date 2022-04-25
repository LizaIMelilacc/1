import json
from utils import get_answer


with open("..\\config.json", 'r', encoding="utf-8") as config_file:
    CONFIG = json.loads('\n'.join(config_file.readlines()))


def handle_dialog(request):
    if request["session"]["new"]:
        # Здороваемся и спрашиваем название/ингредиенты блюда
        return get_answer("greetings")

    command = request["request"]["command"]
    message_id = request["session"]["message_id"]
    if message_id == 1:
        pass
    return command[::-1]
