#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
from threading import Lock


class FlaskServer:
    def __init__(self, rtl_sdr, server_host='0.0.0.0', server_port=8081):
        self.rtl_sdr = rtl_sdr
        self.server_addr = (server_host, server_port)
        self.thread = None
        self.thread_lock = Lock()
        self.index_namespace = '/'
        self.graph_namespace = '/graph'
        self.import_flask()
        self.initialize_flask()

    def import_flask(self):
        try:
            global Flask, render_template, SocketIO, emit
            from flask import Flask, render_template
            from flask_socketio import SocketIO, emit
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
            def page_index(): return render_template('index.html', async_mode=self.socketio.async_mode)
            def page_graph(): return render_template('graph.html', async_mode=self.socketio.async_mode)

            def ping_pong(): emit('server_pong')
            def send_args_index(): self.socketio.emit('client_message', self.rtl_sdr.args, \
                                namespace=self.index_namespace)
            def send_args_settings(): self.socketio.emit('client_message', self.rtl_sdr.args, \
                                namespace=self.settings_namespace)
            def send_args_graph(): self.socketio.emit('cli_args', self.rtl_sdr.args, \
                                namespace=self.graph_namespace)

            self.flask_server = Flask(__name__)
            self.socketio = SocketIO(self.flask_server, async_mode=None)
    
            self.flask_server.route(self.index_namespace)(page_index)
            self.socketio.on('send_args', namespace=self.index_namespace)(send_args_index)

            self.flask_server.route(self.graph_namespace, methods=['GET', 'POST'])(page_graph)
            self.socketio.on('disconnect_request', namespace=self.graph_namespace)(self.disconnect_request)
            self.socketio.on('create_fft_graph', namespace=self.graph_namespace)(self.create_fft_graph)
            self.socketio.on('send_cli_args', namespace=self.graph_namespace)(send_args_graph)
            self.socketio.on('update_settings', namespace=self.graph_namespace)(self.update_settings)
            self.socketio.on('server_ping', namespace=self.graph_namespace)(ping_pong)
            
        except Exception as e:
            print("Could not initialize Flask server.\n" + str(e))
            sys.exit()

    def run(self):
        try:
            self.socketio.run(self.flask_server, 
                host=self.server_addr[0], 
                port=self.server_addr[1])
        except Exception as e:
            print("Failed to run Flask server.\n" + str(e))
            sys.exit()

    def disconnect_request(self):
        disconnect()
        self.socketio.stop()

    def create_fft_graph(self):
        self.send_to_server("Creating FFT graph from samples... [>]")
        with self.thread_lock:
            if self.thread is None:
                self.c_read = True
                self.thread = self.socketio.start_background_task(self.rtlsdr_thread)

    def send_to_server(self, msg, count=0):
        self.socketio.emit(
            'client_message', 
            {'data': msg, 'count': count}, 
            namespace=self.graph_namespace)

    def rtlsdr_thread(self):
        self.rtl_sdr.init_device()
        while self.c_read:
            fft_data = self.rtl_sdr.get_fft_data()
            self.socketio.emit(
            'fft_data', 
            {'data': fft_data}, 
            namespace=self.graph_namespace)
            self.socketio.sleep(0.4)

    def update_settings(self, args):
        self.rtl_sdr.set_args(args)

