# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from vmess2clash import get_clash_sub

app = Flask(__name__)


@app.route("/")
def hello():
    vmess_url = request.args.get('vmess')
    return get_clash_sub(vmess_url)


if __name__ == "__main__":
    app.run(port=5000)
