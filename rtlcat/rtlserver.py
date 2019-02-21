#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys

class FlaskServer:
    def __init__(self, rtl_sdr, server_addr = ('0.0.0.0', 8081)):
        self.rtl_sdr = rtl_sdr
        #self.rtl_sdr.init_device()
        self.server_addr = server_addr
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
            def send_args_graph(): self.socketio.emit('cli_args', 
                                {'args': self.rtl_sdr.args, 'status': 0},
                                namespace=self.graph_namespace)

            self.flask_server = Flask(__name__)
            self.socketio = SocketIO(self.flask_server, async_mode=None)
            self.flask_server.route(self.index_namespace)(page_index)

            self.flask_server.route(self.graph_namespace, methods=['GET', 'POST'])(page_graph)
            self.socketio.on('connect', namespace=self.graph_namespace)(self.socketio_on_connect)
            self.socketio.on('disconnect_request', namespace=self.graph_namespace)(self.disconnect_request)
            self.socketio.on('create_fft_graph', namespace=self.graph_namespace)(self.create_fft_graph)
            self.socketio.on('send_cli_args', namespace=self.graph_namespace)(send_args_graph)
            self.socketio.on('update_settings', namespace=self.graph_namespace)(self.update_settings)
            self.socketio.on('stop_sdr', namespace=self.graph_namespace)(self.stop_sdr)
            self.socketio.on('server_ping', namespace=self.graph_namespace)(ping_pong)
            
        except Exception as e:
            print("Could not initialize Flask server.\n" + str(e))
            sys.exit()

    def run(self):
        try:
            self.socketio.run(self.flask_server, 
                host=self.server_addr[0], 
                port=int(self.server_addr[1]))
        except Exception as e:
            print("Failed to run Flask server.\n" + str(e))
            sys.exit()

    def socketio_on_connect(self):
        self.thread = self.socketio.start_background_task(self.rtl_sdr.init_device)

    def disconnect_request(self):
        self.socketio.stop()

    def stop_sdr(self):
        self.c_read = False
        self.n_read = 0

    def create_fft_graph(self):
        if self.rtl_sdr.dev == None:
            self.socketio.emit(
            'client_message', 
            {'data': 'Failed to open & initialize RTL-SDR device.'}, 
            namespace=self.graph_namespace)
            self.socketio_on_connect()
        else:
            self.socketio.emit(
                'client_message', 
                {'data': 'Creating FFT graph from samples...'}, 
                namespace=self.graph_namespace)
            self.c_read = True
            self.thread = self.socketio.start_background_task(self.rtlsdr_thread)


    def update_settings(self, args):
        self.rtl_sdr.set_args(args)
        self.socketio.emit('cli_args', {'args': self.rtl_sdr.args, 'status': 1}, \
                                namespace=self.graph_namespace)

    def rtlsdr_thread(self):
        self.n_read = self.rtl_sdr.num_read
        interval = int(self.rtl_sdr.interval) / 1000.0
        while self.c_read:
            fft_data = self.rtl_sdr.get_fft_data()
            self.socketio.emit(
            'fft_data', 
            {'data': fft_data}, 
            namespace=self.graph_namespace)
            self.socketio.sleep(interval)
            self.n_read-=1
            if self.n_read == 0: break


