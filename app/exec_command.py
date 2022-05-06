import app.api as api
from app import store
from app.utils import *
from app.AnswerTypes import *
from app.kewords import Keywords


def contain(phrase: set, phrase_type: set) -> bool:
    return len(phrase.intersection(phrase_type)) != 0


def prepare_response(response, request):
    response["session_state"]["current_state"] = request["state"]["session"]["current_state"]
    response["session_state"]["bad"] = request["state"]["session"]["bad"]
    response["session_state"]["good"] = request["state"]["session"]["good"]
    response["session_state"]["current_recipe_id"] = request["state"]["session"]["current_recipe_id"]


def exec_command(response, cmd, request):
    """
    parse params and execute
    :param response: json-response
    :param cmd: command
    :param request: json-request (from Alice server)
    :return: None. change values in response
    """
    command = [to_normal_form(word) for word in cmd.lower().split()]
    command_set = set(command)
    prepare_response(response, request)
    user_data = store.UserData(response)
    if cmd.lower() == "подробнее":
        set_text(response, "Открываю")
    if cmd in Keywords.HELP:
        set_text(response, get_answer_option("help"))
        user_data.dialog_point = AnswerTypes.START
        user_data.commit(response)
    match user_data.dialog_point:
        case AnswerTypes.WELCOME:
            user_data.bad = []  # При перезапуске отменяем стоп-лист
            set_text(response, get_answer_option("type_of_searching"))
            set_buttons(response, ["список", "название", "исключить"])
            user_data.dialog_point = AnswerTypes.START
            user_data.commit(response)  # Сохраняем все изменения
            return
        case AnswerTypes.START:
            if contain(command_set, Keywords.BAD_LIST):
                user_data.dialog_point = AnswerTypes.SET_BAD
                set_text(response, get_answer_option('bad_ingredients'))
            elif contain(command_set, Keywords.TITLE_SEARCH):
                user_data.dialog_point = AnswerTypes.FIND_NAME
                set_text(response, get_answer_option('title'))
            elif contain(command_set, Keywords.LIST_SEARCH):
                user_data.dialog_point = AnswerTypes.FIND_LIST
                set_text(response, get_answer_option('ingredients'))
            else:
                set_text(response, get_answer_option("not_understand") + \
                         "\n" + get_answer_option("will_repeat"))
                set_buttons(response, ["да", "нет"], hide=True)
        case AnswerTypes.SET_BAD:
            if contain({cmd}, Keywords.STOP_WORD):
                user_data.dialog_point = AnswerTypes.START  # Добавить кнопки - оценить, повторить и в начало
                set_text(response, get_answer_option('type_of_searching'))
                set_buttons(response, ["список", "название"])
            else:
                user_data.bad.append(cmd.lower())
                set_text(response, get_answer_option('next'))
        case AnswerTypes.FIND_LIST:
            if contain({cmd}, Keywords.STOP_WORD):
                recipe = api.get_by_ingredients(user_data.good, user_data.bad)
                api.show_recipe(response, recipe)
                if recipe != {}:
                    user_data.current_recipe_id = recipe['RecipeId']
                    set_buttons(response, ["оценить", "повтор", "стоп"])
                else:
                    set_buttons(response, ["стоп"])
                user_data.dialog_point = AnswerTypes.SEARCH  # Добавить кнопки - оценить, повторить и в начало
            else:
                user_data.good.append(cmd.lower())
                set_text(response, get_answer_option('next'))
        case AnswerTypes.FIND_NAME:
            recipe = api.get_by_title(user_data.good, user_data.bad)
            api.show_recipe(response, recipe)
            if recipe != {}:
                user_data.current_recipe_id = recipe['RecipeId']
                set_buttons(response, ['оценить', "повтор", "стоп"])
            else:
                set_buttons(response, ["стоп"])
            user_data.dialog_point = AnswerTypes.SEARCH
        case AnswerTypes.SEARCH:
            if contain({cmd}, Keywords.REPEAT):
                recipe = api.get_by_id(user_data.current_recipe_id)
                api.show_recipe(response, recipe)
                if recipe != {}:
                    set_buttons(response, ["оценить", "повтор", "стоп"])
                else:
                    set_buttons(response, ["стоп"])
            elif contain({cmd}, Keywords.RATE):
                user_data.dialog_point = AnswerTypes.SET_RATE
                set_text(response, get_answer_option('rate'))
                set_buttons(response, [str(i) for i in range(5, 0, -1)])
            else:
                user_data.dialog_point = AnswerTypes.WILL_REPEAT
                set_text(response, get_answer_option('will_repeat'))
                set_buttons(response, ["да", "нет"])
        case AnswerTypes.SET_RATE:
            if cmd.isdigit():
                api.send_rate(user_data.current_recipe_id, int(cmd))
            user_data.dialog_point = AnswerTypes.WILL_REPEAT
            set_text(response, get_answer_option('will_repeat'))
            set_buttons(response, ["да", "нет"], hide=True)
        case AnswerTypes.WILL_REPEAT:
            if cmd.lower() in Keywords.ACCEPT:
                user_data.dialog_point = AnswerTypes.START
                set_text(response, get_answer_option("type_of_searching"))
                set_buttons(response, ["список", "название", "исключить"])
            else:
                set_text(response, "До связи")
                response['end_session'] = True
    user_data.commit(response)  # Сохраняем все изменения
