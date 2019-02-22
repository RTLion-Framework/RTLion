#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
from logcl import LogCL

class FlaskServer:
    def __init__(self, rtl_sdr, server_addr = ('0.0.0.0', 8081)):
        self.logcl = LogCL()
        self.rtl_sdr = rtl_sdr
        self.server_addr = server_addr
        self.index_namespace = '/'
        self.graph_namespace = '/graph'
        self.routes = (self.index_namespace, self.graph_namespace)
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

    def add_route(self, rule, func):
        try:
            self.flask_server.add_url_rule(rule, func.__name__, func)
        except Exception as e:
            self.logcl.log("Failed to add URL rule.\n" + str(e), 'error')
            sys.exit()

    def initialize_flask(self):
        self.logcl.log("Initializing Flask server with routes: " + str(self.routes))
        try:
            def page_index(): return render_template('index.html', async_mode=self.socketio.async_mode)
            def page_graph(): return render_template('graph.html', async_mode=self.socketio.async_mode)

            def ping_pong(): emit('server_pong')
            def send_args_graph(): self.socketio.emit('cli_args', 
                                {'args': self.rtl_sdr.args, 'status': 0},
                                namespace=self.graph_namespace)
            def socketio_on_connect():
                self.start_sdr()
            def socketio_on_disconnect():
                self.socketio.stop()

            self.flask_server = Flask(__name__)
            self.socketio = SocketIO(self.flask_server, async_mode=None)
            self.flask_server.route(self.index_namespace)(page_index)

            self.flask_server.route(self.graph_namespace, methods=['GET', 'POST'])(page_graph)
            self.socketio.on('connect', namespace=self.graph_namespace)(socketio_on_connect)
            self.socketio.on('disconnect_request', namespace=self.graph_namespace)(socketio_on_disconnect)
            self.socketio.on('create_fft_graph', namespace=self.graph_namespace)(self.create_fft_graph)
            self.socketio.on('send_cli_args', namespace=self.graph_namespace)(send_args_graph)
            self.socketio.on('update_settings', namespace=self.graph_namespace)(self.update_settings)
            self.socketio.on('stop_sdr', namespace=self.graph_namespace)(self.stop_sdr)
            self.socketio.on('server_ping', namespace=self.graph_namespace)(ping_pong)
            
        except Exception as e:
            self.logcl.log("Could not initialize Flask server.\n" + str(e), 'error')
            sys.exit()

    def run(self):
        self.logcl.log("Running server: http://" + self.server_addr[0] + ":" + self.server_addr[1])
        try:
            self.socketio.run(self.flask_server, 
                host=self.server_addr[0], 
                port=int(self.server_addr[1]))
        except Exception as e:
            self.logcl.log("Failed to run Flask server.\n" + str(e), 'fatal')
            sys.exit()

    def stop_sdr(self):
        self.logcl.log("Stop reading samples from RTL-SDR...")
        self.c_read = False
        self.n_read = 0
    
    def start_sdr(self):
        if not self.rtl_sdr.dev_open:
            self.socketio.start_background_task(self.rtl_sdr.init_device)

    def create_fft_graph(self):
        if self.rtl_sdr.dev == None:
            self.start_sdr()
        else:
            self.logcl.log("Creating FFT graph from samples...")
            self.c_read = True
            self.socketio.start_background_task(self.rtlsdr_thread)

    def update_settings(self, args):
        try:
            self.rtl_sdr.set_args(args)
            self.socketio.emit('cli_args', {'args': self.rtl_sdr.args, 'status': 1}, \
                                    namespace=self.graph_namespace)
            self.logcl.log("Settings/arguments updated.")
        except:
            self.logcl.log("Failed to update settings.", 'error')

    def rtlsdr_thread(self):
        self.n_read = self.rtl_sdr.num_read
        interval = int(self.rtl_sdr.interval) / 1000.0
        self.logcl.log("Getting graph data with interval " + 
        str(interval) + " (" + str(self.n_read) + "x)")
        while self.c_read:
            fft_data = self.rtl_sdr.get_fft_data()
            self.socketio.emit(
            'fft_data', 
            {'data': fft_data}, 
            namespace=self.graph_namespace)
            self.socketio.sleep(interval)
            self.n_read-=1
            if self.n_read == 0: break
    
    def socket_log(self, msg, ns=1):
        self.socketio.emit('log_message', {'msg': msg}, namespace=self.routes[ns])


