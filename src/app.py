from flask import Flask, request
import logging

from handler import handle_dialog


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/', methods=["POST", "GET"])
def main():
    req = request.json
    response = {
        "version": req["version"],
        "session": req["session"],
        "response": {
            "end_session": False,
            "text": handle_dialog(req)
        }
    }

    return response


if __name__ == '__main__':
    port = 8000
    app.run(host='127.0.0.1', port=port)
