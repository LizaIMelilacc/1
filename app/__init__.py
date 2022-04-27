from flask import Flask, request, Response
import logging
import json
from app.utils import *
from dotenv import load_dotenv
import os

load_dotenv()
CONFIG = load_config()
app = Flask(__name__)
logging.basicConfig(filename="app/logs/alice.log", filemode='w', level=logging.INFO)


@app.route('/', methods=['POST'])
def main():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    try:
        handle_dialog(request.json, response)
    except Exception as error:
        logging.error(f'ERR:  {error!r}')
        response['response']['text'] = CONFIG['error']
    return Response(json.dumps(response), mimetype='application/json')


def handle_dialog(req, res):
    set_text(res, 'hi')
    if req['session']['new']:  # is sessions new?
        set_text(res, get_answer_option("greetings"))
    else:
        exec_command(res, req['request']['command'])


port = int(os.environ.get('PORT', 5000))
