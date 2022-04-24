from flask import Flask, request, Response
import logging
import json
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/skill/', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response)
    logging.info(f'Response:  {response!r}')
    return Response(json.dumps(response), mimetype='application/json')


def handle_dialog(req, res):
    res['response']['text'] = "hi"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
