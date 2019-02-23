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

            self.flask_server = Flask(__name__)
            self.socketio = SocketIO(self.flask_server, async_mode=None)
            self.flask_server.route(self.index_namespace)(page_index)
            self.flask_server.route(self.graph_namespace, methods=['GET', 'POST'])(page_graph)
            self.socketio.on('connect', namespace=self.graph_namespace)(self.socketio_on_connect)
            self.socketio.on('disconnect_request', namespace=self.graph_namespace)(self.socketio_on_disconnect)
            self.socketio.on('start_sdr', namespace=self.graph_namespace)(self.start_sdr)
            self.socketio.on('stop_sdr', namespace=self.graph_namespace)(self.stop_sdr)
            self.socketio.on('send_cli_args', namespace=self.graph_namespace)(self.send_args_graph)
            self.socketio.on('update_settings', namespace=self.graph_namespace)(self.update_settings)
            self.socketio.on('server_ping', namespace=self.graph_namespace)(self.ping_pong)
            
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

    def socketio_on_connect(self):
        self.socket_log("RTLion started.")

    def socketio_on_disconnect(self):
        self.logcl.log("Stopping server...")
        self.socketio.stop()

    def ping_pong(self): 
        self.socketio.emit('server_pong', namespace=self.graph_namespace)

    def start_sdr(self):
        if not self.rtl_sdr.dev_open:
            if(self.rtl_sdr.init_device()):
                self.socket_log("RTL-SDR device opened. [#" + str(self.rtl_sdr.dev_id) + "]")
                self.create_fft_graph()
            else:
                self.socket_log("Failed to open RTL-SDR device. [#" + str(self.rtl_sdr.dev_id) + "]")
                self.socketio.emit('dev_status', 0, namespace=self.graph_namespace)
        else:
            self.create_fft_graph()

    def stop_sdr(self):
        self.logcl.log("Stop reading samples from RTL-SDR.")
        self.socket_log("Stop reading samples from RTL-SDR.")
        self.socketio.emit('dev_status', 0, namespace=self.graph_namespace)
        self.c_read = False
        self.n_read = 0

    def send_args_graph(self, status=0): 
        self.socketio.emit(
            'cli_args', 
            {'args': self.rtl_sdr.args, 'status': status},
            namespace=self.graph_namespace)

    def update_settings(self, args):
        try:
            self.rtl_sdr.set_args(args)
            self.send_args_graph(1)
            self.logcl.log("Settings/arguments updated.")
            self.socket_log("Settings/arguments updated.")
        except:
            self.logcl.log("Failed to update settings.", 'error')

    def create_fft_graph(self):
        self.socketio.emit('dev_status', 1, namespace=self.graph_namespace)
        self.socket_log("Creating FFT graph from samples...")
        self.logcl.log("Creating FFT graph from samples...")
        self.c_read = True
        self.socketio.start_background_task(self.rtlsdr_thread)

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


