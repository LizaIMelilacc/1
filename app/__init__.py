from flask import Flask, request, Response
import logging
import json
from app.utils import *
from app.exec_command import exec_command
from dotenv import load_dotenv
from app.Env import Env

load_dotenv()
CONFIG = config
app = Flask(__name__)
logging.basicConfig(filename=Env.LOG_FILE, filemode=Env.LOG_MODE, level=logging.INFO)


@app.route('/', methods=['POST'])
def main():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response)
    return Response(json.dumps(response), mimetype='application/json')


def handle_dialog(req, res):
    if req['session']['new']:  # is sessions new?
        set_text(res, get_answer_option('greetings'))
    else:
        exec_command(res, req['request']['command'])


port = Env.PORT
