#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys

class FlaskServer:
    def __init__(self, server_host='0.0.0.0', server_port=8081):
        self.server_addr = (server_host, server_port)
        self.import_flask()
        self.initialize_flask()

    def import_flask(self):
        try:
            global Flask, request, jsonify
            from flask import Flask, request, jsonify
        except:
            print("Flask framework not found.")
            sys.exit()

    def add_route(self, rule, func):
        try:
            self.flask_server.add_url_rule(rule, func.__name__, func)
        except Exception as e:
            print("Failed to add URL rule.\n" + str(e))
            sys.exit()

    def initialize_flask(self):
        try:
            self.flask_server = Flask(__name__)
            self.add_route("/", self.page_index)
        except Exception as e:
            print("Could not initialize Flask server.\n" + str(e))
            sys.exit()

    def run(self):
        try:
            self.flask_server.run(host=self.server_addr[0], 
                                port=self.server_addr[1])
        except Exception as e:
            print("Failed to run Flask server.\n" + str(e))
            sys.exit()

    def page_index(self):

        return "rtl_cat"
