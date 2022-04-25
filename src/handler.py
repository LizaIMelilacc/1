def handle_dialog(request):
    if request["session"]["new"]:
        return "Здравствуйте! Я попугай"

    command = request["request"]["command"]
    response_text = command[::-1]

    return response_text
