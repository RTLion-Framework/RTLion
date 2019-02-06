#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from rtlcat.rtldev import RTLSdr
from rtlcat.argparser import parse_cli_args
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "~"


def main():

    app.run(host='0.0.0.0', port=5000)

    #rtl_sdr = RTLSdr(**parse_cli_args())
    #rtl_sdr.create_graph(True, 100)
    #rtl_sdr.close()
1
if __name__ == "__main__":
    main()