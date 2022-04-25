from flask import Flask, request
import logging
from utils import get_answer

from handler import handle_dialog


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/', methods=["POST"])
def main():
    req = request.json

    try:
        answer = handle_dialog(req)
    except Exception as error:
        logging.error(f'ERR:  {error!r}')
        answer = get_answer("error")
    response = {
        "version": req["version"],
        "session": req["session"],
        "response": {
            "end_session": False,
            "text": answer
        }
    }

    return response


if __name__ == '__main__':
    port = 8000
    app.run(host='127.0.0.1', port=port)
