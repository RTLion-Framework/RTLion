#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
from logcl import LogCL
from rtlsocket import RTLSocket

class FlaskServer:
    def __init__(self, rtl_sdr, server_addr = ('0.0.0.0', 8081)):
        self.logcl = LogCL()
        self.rtl_sdr = rtl_sdr
        self.server_addr = server_addr
        self.import_flask()
        self.initialize_flask()

    def import_flask(self):
        try:
            self.logcl.log("Importing Flask & SocketIO...")
            global Flask, render_template, SocketIO, emit
            from flask import Flask, render_template
            from flask_socketio import SocketIO, emit
        except Exception as e:
            self.logcl.log("Flask & SocketIO not found.\n" + str(e), 'error')
            sys.exit()

    def initialize_flask(self):
        self.routes = RTLSocket(None, None, self.logcl).get_routes()
        self.logcl.log("Initializing Flask server with routes: " + str(self.routes))
        try:
            self.flask_server = Flask(__name__)
            self.socketio = SocketIO(self.flask_server, async_mode=None)
            self.rtlSocket = RTLSocket(self.socketio, self.rtl_sdr, self.logcl)
            self.rtlSocket.add_templates(self.flask_server, render_template)
            self.rtlSocket.add_namespace(0, 
                ('get_dev_status',
                'disconnect_request'))
            self.rtlSocket.add_namespace(1, 
                ('connect',
                'disconnect_request',
                'start_sdr',
                'stop_sdr',
                'restart_sdr',
                'start_scan',
                'send_cli_args',
                'update_settings',
                'server_ping'))
            self.rtlSocket.add_namespace(3, 
                ('send_app_args',
                'update_app_settings',
                'get_fft_graph',
                'get_scanned_values'))
        except Exception as e:
            self.logcl.log("Could not initialize Flask server.\n" + str(e), 'error')
            sys.exit()
            
    def run(self):
        self.logcl.log("Running server: http://" + \
            self.server_addr[0] + \
            ":" + self.server_addr[1])
        try:
            self.socketio.run(self.flask_server, 
                host=self.server_addr[0], 
                port=int(self.server_addr[1]))
        except KeyboardInterrupt:
            RTLSocket(self.socketio, self.rtl_sdr, self.logcl).disconnect_request()
        except Exception as e:
            self.logcl.log("Failed to run Flask server.\n" + str(e), 'fatal')
            sys.exit()
