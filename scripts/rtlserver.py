#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
import json
from logcl import LogCL
from rtlns import RTLNs

class FlaskServer:
    def __init__(self, rtl_sdr, server_addr = ('0.0.0.0', 8081)):
        self.logcl = LogCL()
        self.rtl_sdr = rtl_sdr
        self.server_addr = server_addr
        self.import_flask()
        self.initialize_flask1()

    def import_flask(self):
        try:
            self.logcl.log("Importing Flask & SocketIO...")
            global Flask, render_template, SocketIO, emit
            from flask import Flask, render_template
            from flask_socketio import SocketIO, emit
        except Exception as e:
            self.logcl.log("Flask & SocketIO not found.\n" + str(e), 'error')
            sys.exit()

    def initialize_flask1(self):
        self.routes = RTLNs(None, None, self.logcl).get_routes()
        self.logcl.log("Initializing Flask server with routes: " + str(self.routes))
        try:
            self.flask_server = Flask(__name__)
            self.socketio = SocketIO(self.flask_server, async_mode=None)
            self.rtlNs = RTLNs(self.socketio, self.rtl_sdr, self.logcl)
            @self.flask_server.route(self.routes[0], methods=['GET', 'POST'])
            def index_page(): return render_template('index.html', 
                async_mode=self.socketio.async_mode)
            self.rtlNs.add_namespace(0, 
                ('get_dev_status',
                'disconnect_request'))
            @self.flask_server.route(self.routes[1], methods=['GET', 'POST'])
            def graph_page(): return render_template('graph.html', 
                async_mode=self.socketio.async_mode)
            self.rtlNs.add_namespace(1, 
                ('connect',
                'disconnect_request',
                'start_sdr',
                'stop_sdr',
                'restart_sdr',
                'start_scan',
                'send_cli_args',
                'update_settings',
                'server_ping'))
            @self.flask_server.route(self.routes[2], methods=['GET', 'POST'])
            def scan_page(): return render_template('scan.html', 
                async_mode=self.socketio.async_mode)
            @self.flask_server.route(self.routes[3], methods=['GET', 'POST'])
            def app_page(): return render_template('app.html', 
                async_mode=self.socketio.async_mode)
            self.rtlNs.add_namespace(3, 
                ('send_app_args',
                'update_app_settings',
                'get_fft_graph',
                'get_scanned_values'))

        except Exception as e:
            self.logcl.log("Could not initialize Flask server.\n" + str(e), 'error')
            sys.exit()

    def initialize_flask(self):
        self.logcl.log("Initializing Flask server with routes: " + str(self.routes))
        try:
            def page_index(): return render_template('index.html', async_mode=self.socketio.async_mode)
            def page_graph(): return render_template('graph.html', async_mode=self.socketio.async_mode)
            def page_scan(): return render_template('scan.html', async_mode=self.socketio.async_mode)
            def page_app(): return render_template('app.html', async_mode=self.socketio.async_mode)
            self.flask_server = Flask(__name__)
            self.socketio = SocketIO(self.flask_server, async_mode=None)
            self.flask_server.route(self.index_namespace,  methods=['GET', 'POST'])(page_index)
            self.socketio.on('get_dev_status', namespace=self.index_namespace)(self.get_dev_status)
            self.socketio.on('disconnect_request', namespace=self.index_namespace)(self.disconnect_request)
            self.flask_server.route(self.graph_namespace, methods=['GET', 'POST'])(page_graph)
            self.socketio.on('connect', namespace=self.graph_namespace)(self.connect)
            self.socketio.on('disconnect_request', namespace=self.graph_namespace)(self.disconnect_request)
            self.socketio.on('start_sdr', namespace=self.graph_namespace)(self.start_sdr)
            self.socketio.on('stop_sdr', namespace=self.graph_namespace)(self.stop_sdr)
            self.socketio.on('restart_sdr', namespace=self.graph_namespace)(self.restart_sdr)
            self.socketio.on('start_scan', namespace=self.graph_namespace)(self.start_scan)
            self.socketio.on('send_cli_args', namespace=self.graph_namespace)(self.send_cli_args)
            self.socketio.on('update_settings', namespace=self.graph_namespace)(self.update_settings)
            self.socketio.on('server_ping', namespace=self.graph_namespace)(self.server_ping)
            self.flask_server.route(self.app_namespace)(page_app)
            self.socketio.on('send_app_args', namespace=self.app_namespace)(self.send_app_args)
            self.socketio.on('update_app_settings', namespace=self.app_namespace)(self.update_app_settings)
            self.socketio.on('get_fft_graph', namespace=self.app_namespace)(self.get_fft_graph)
            self.socketio.on('get_scanned_values', namespace=self.app_namespace)(self.get_scanned_values)
            self.flask_server.route(self.scan_namespace, methods=['GET', 'POST'])(page_scan)
            
        except Exception as e:
            self.logcl.log("Could not initialize Flask server.\n" + str(e), 'error')
            sys.exit()

    def run(self):
        self.logcl.log("Running server: http://" + self.server_addr[0] + ":" + self.server_addr[1])
        try:
            self.socketio.run(self.flask_server, 
                host=self.server_addr[0], 
                port=int(self.server_addr[1]))
        except KeyboardInterrupt:
            RTLNs(self.socketio, self.rtl_sdr, self.logcl).disconnect_request()
        except Exception as e:
            self.logcl.log("Failed to run Flask server.\n" + str(e), 'fatal')
            sys.exit()
                
