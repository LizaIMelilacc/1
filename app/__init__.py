from flask import Flask, request, Response
import logging
import json
from app.utils import *
from app.exec_command import exec_command
from dotenv import load_dotenv
from app.Env import Env
from app.store import TestUserData

load_dotenv()
CONFIG = config
app = Flask(__name__)
logging.basicConfig(filename=Env.LOG_FILE, filemode=Env.LOG_MODE, level=logging.INFO)


TEST_USER_DATA = None


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
    if req['session']['new']:  # is sessions new?
        global TEST_USER_DATA
        TEST_USER_DATA = TestUserData(req['session']['user']['user_id'])
        set_text(res, get_answer_option('greetings'))
    else:
        exec_command(res, req['request']['command'], TEST_USER_DATA)


port = Env.PORT
