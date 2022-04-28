from utils import *


def exec_command(response, cmd):
    """
    parse params and execute
    :param response: json-response
    :param cmd: command
    :return: None. change values in response
    """
    command = set([to_normal_form(word) for word in cmd.lower().split()])

    help_words = {"сначала", "заново", "перезапустить", "помощь"}
    # refusal_words = {"нет"}
    # agreement_words = {"да", "согласный", "хотеть"}
    # continuation_words = {"следующий", "шаг", "продолжить"}

    user_id = response["session"]["user_id"]
    previous_answer = AnswerTypes.from_string(load_answer(user_id))
    bad_list = get_user_bad(user_id)
    if command <= help_words:
        set_text(response, get_answer_option("help"))
        save_answer(user_id, AnswerTypes.HELP)
    elif previous_answer == AnswerTypes.SET_BAD_LIST:
        bad_list = get_bad_list(cmd)  # Тут получим bad-list, обработав command.
        set_user_bad(user_id, bad_list)
        set_text(response, "Ищем рецепт по названию или имеющимся ингредиентам?")
        save_answer(user_id, AnswerTypes.SET_TYPE_OF_SEARCHING)
    elif previous_answer == AnswerTypes.SET_TYPE_OF_SEARCHING:
        if {"ингредиент", "ингредиенты"} & command:
            set_text(response, get_answer_option("ingredients"))
            save_answer(user_id, AnswerTypes.SET_INGREDIENTS)
        elif {'название'} & command:
            set_text(response, get_answer_option("title"))
            save_answer(user_id, AnswerTypes.SET_TITLE)
        else:
            set_text(response,
                     "Не поняла вас. Напишите, пожалуйста, как вы хотите искать рецепт: по названию блюда или ингредиентам?")
    elif previous_answer == AnswerTypes.SET_TITLE:
        title = get_title(cmd)  # Тут получим title, обработав command.
        recipe = get_by_title(title, bad_list)  # Нужно получить id рецепта для дальнейшего его сохранения в бд.
        set_text(response, pretty_recipe(recipe))
    elif previous_answer == AnswerTypes.SET_INGREDIENTS:
        ingredients = get_ingredients(cmd)  # Тут получим ingredients, обработав command.
        recipe = get_by_ingredients(ingredients, bad_list)
        set_text(response, pretty_recipe(recipe))
    elif previous_answer == AnswerTypes.SET_RATE:
        rate = int(cmd)  # Примитивное получение рейтинга. Работает, когда cmd - число.
        send_rate(rate)
    # Не доделано
