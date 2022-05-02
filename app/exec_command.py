from app.api import get_by_title, pretty_recipe, send_rate, get_by_ingredients
from app.utils import *
from app.AnswerTypes import *


def exec_command(response, cmd):
    """
    parse params and execute
    :param response: json-response
    :param cmd: command
    :return: None. change values in response
    """
    command = set([to_normal_form(word) for word in cmd.lower().split()])

    restart_words = {"сначала", "заново", "перезапустить", "в"}
    repeat_words = {"повторить", "еще"}
    refusal_words = {"нет", "отутствовать", "отказать"}
    agreement_words = {"да", "согласный", "начать"}
    # continuation_words = {"следующий", "шаг", "продолжить"}

    user_id = response["session"]['user']["user_id"]
    previous_answer = AnswerTypes.from_string(store.load_answer(user_id))
    bad_list = store.get_user_data(user_id)[store.BAD_LIST_ID]
    if cmd == "помощь":
        set_text(response, get_answer_option("help"))
    elif command <= restart_words:
        go_to_start(response, user_id)
    elif previous_answer == AnswerTypes.START:
        set_text(response, get_answer_option("bad_ingredients"))
        store.save_answer(user_id, AnswerTypes.SET_BAD_LIST)
    elif previous_answer == AnswerTypes.SET_BAD_LIST:
        if command & refusal_words:
            bad_list = []
        else:
            bad_list = get_ingredients(cmd)  # Тут получим bad-list, обработав command.
        store.set_user_bad(user_id, bad_list)
        set_text(response, get_answer_option("type_of_searching"))
        store.save_answer(user_id, AnswerTypes.SET_TYPE_OF_SEARCHING)
    elif previous_answer == AnswerTypes.SET_TYPE_OF_SEARCHING:
        if {"ингредиент", "ингредиенты"} & command:
            set_text(response, get_answer_option("ingredients"))
            store.save_answer(user_id, AnswerTypes.SET_INGREDIENTS)
        elif {'название'} & command:
            set_text(response, get_answer_option("title"))
            store.save_answer(user_id, AnswerTypes.SET_TITLE)
        else:
            set_text(response,
                     get_answer_option("not_understand") + ' ' + get_answer_option("type_of_searching"))
    elif previous_answer == AnswerTypes.SET_TITLE:
        title = get_title(cmd)  # Тут получим title, обработав command.
        recipe = get_by_title(title, bad_list)  # Нужно получить id рецепта для дальнейшего его сохранения в бд.
        set_text(response, pretty_recipe(recipe))
        store.save_recipe(user_id, recipe)
        store.save_answer(user_id, AnswerTypes.RECIPE)
    elif previous_answer == AnswerTypes.SET_INGREDIENTS:
        ingredients = get_ingredients(cmd)  # Тут получим ingredients, обработав command.
        recipe = get_by_ingredients(ingredients, bad_list)
        set_text(response, pretty_recipe(recipe))
        store.save_recipe(user_id, recipe)
        store.save_answer(user_id, AnswerTypes.RECIPE)
    elif previous_answer == AnswerTypes.RECIPE:
        if command and repeat_words:
            recipe = store.load_recipe(user_id)
            set_text(response, pretty_recipe(recipe))
        else:
            set_text(response, get_answer_option("will_rate"))
            store.save_answer(user_id, AnswerTypes.WILL_RATE)
    elif previous_answer == AnswerTypes.WILL_RATE:
        if command & agreement_words:
            set_text(response, get_answer_option("rate"))
            store.save_answer(user_id, AnswerTypes.SET_RATE)
        elif command & refusal_words:
            set_text(response, "Хорошо. " + get_answer_option("will_repeat"))
            store.save_answer(response, AnswerTypes.WILL_REPEAT)
        else:
            set_text(response, get_answer_option("not_understand") + ' ' + get_answer_option("will_rate"))
    elif previous_answer == AnswerTypes.SET_RATE:
        rate = int(cmd)  # Примитивное получение рейтинга. Работает, когда cmd - число.
        send_rate(rate)
        set_text(response, "Спасибо за оценку. " + get_answer_option("repeat"))
        store.save_answer(user_id, AnswerTypes.WILL_REPEAT)
    elif previous_answer == AnswerTypes.WILL_REPEAT:
        if command & agreement_words:
            go_to_start(response, user_id)
    else:
        raise ValueError("Previous answer is not instance of AnswerTypes.")
