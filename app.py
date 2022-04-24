from flask import Flask, request, Response
import logging
import json
import os
from utils import *

with open('config.json', 'r', encoding="utf-8") as config_file:
    CONFIG = json.loads('\n'.join(config_file.readlines()))
app = Flask(__name__)
logging.basicConfig(filename="alice.log", level=logging.INFO)


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
        set_text(res, CONFIG['greeting'].format(CONFIG["name"]))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
