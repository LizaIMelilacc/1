from flask import Flask, request, Response
import logging
import json
import os
from app.utils import *
from app.read_config import config

app = Flask(__name__)
logging.basicConfig(filename="alice.log", filemode=os.getenv("LOG_MODE"), level=logging.INFO)


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
        response['response']['text'] = config['error']
    return Response(json.dumps(response), mimetype='application/json')


def handle_dialog(req, res):
    if req['session']['new']:  # is sessions new?
        set_text(res, config['greeting'].format(config["name"]))
    else:
        exec_command(res, req['request']['command'])


port = int(os.environ.get('PORT', 5000))
from app.store import *

set_user_bad('foo', ['1', '4'])
print(get_user_bad('foo'))
print(store.ttl('foo'))
time.sleep(1)
print(get_user_bad('foo'))
