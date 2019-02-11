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
        self.server_namespace = '/graph'
        self.import_flask()
        self.initialize_flask()

    def import_flask(self):
        try:
            global Flask, render_template, session, request, SocketIO, emit, disconnect
            from flask import Flask, render_template, session, request
            from flask_socketio import SocketIO, emit, disconnect
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
            self.socketio = SocketIO(self.flask_server, async_mode=None)
            self.add_route('/', self.page_index)
            self.flask_server.route('/graph')(self.page_graph)     
            self.socketio.on('connect', namespace=self.server_namespace)(self.server_connect)
            self.socketio.on('disconnect', namespace=self.server_namespace)(self.server_disconnect)
            self.socketio.on('server_response', namespace=self.server_namespace)(self.server_response)
            self.socketio.on('disconnect_request', namespace=self.server_namespace)(self.disconnect_request)
            self.socketio.on('create_fft_graph', namespace=self.server_namespace)(self.create_fft_graph)
            self.socketio.on('server_ping', namespace=self.server_namespace)(self.ping_pong)
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

    def page_index(self):
        return "rtl_cat"

    def page_graph(self):
        return render_template('index.html', async_mode=self.socketio.async_mode)

    def server_connect(self):
        self.send_to_server("Connected")

    def disconnect_request(self):
        session['receive_count'] = session.get('receive_count', 0) + 1
        self.send_to_server("Disconnected!", session['receive_count'])
        disconnect()

    def server_disconnect(self):
        print('Client disconnected', request.sid)

    def server_response(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        self.send_to_server(message['data'], session['receive_count'])

    def create_fft_graph(self):
        self.send_to_server("Creating FFT graph from samples...")
        with self.thread_lock:
            if self.thread is None:
                self.thread = self.socketio.start_background_task(self.rtlsdr_thread)

    def send_to_server(self, msg, count=0):
        self.socketio.emit(
            'client_message', 
            {'data': msg, 'count': count}, 
            namespace=self.server_namespace)

    def ping_pong(self):
        emit('server_pong')

    def rtlsdr_thread(self):
        while True:
            fft_data = self.rtl_sdr.get_fft_data()
            self.socketio.emit(
            'fft_data', 
            {'data': fft_data}, 
            namespace=self.server_namespace)
            self.socketio.sleep(0.4)

