from flask import Flask, request, Response
import logging
import json
from read_config import load_config
from utils import *
from dotenv import load_dotenv

load_dotenv()
CONFIG = load_config()
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
        response['response']['text'] = CONFIG['error']
    return Response(json.dumps(response), mimetype='application/json')


def handle_dialog(req, res):
    set_text(res, 'hi')
    if req['session']['new']:  # is sessions new?
        set_text(res, CONFIG['greeting'].format(CONFIG["name"]))
    else:
        exec_command(res, req['request']['command'])


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
