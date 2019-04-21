#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
import json
from logcl import LogCL

class FlaskServer:
    def __init__(self, rtl_sdr, server_addr = ('0.0.0.0', 8081)):
        self.logcl = LogCL()
        self.rtl_sdr = rtl_sdr
        self.server_addr = server_addr
        self.index_namespace = '/'
        self.graph_namespace = '/graph'
        self.app_namespace = '/app'
        self.scan_namespace = '/scan'
        self.routes = (
            self.index_namespace, 
            self.graph_namespace,
            self.app_namespace,
            self.scan_namespace
        )
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
            def page_scan(): return render_template('scan.html', async_mode=self.socketio.async_mode)
            def page_app(): return render_template('app.html', async_mode=self.socketio.async_mode)
            self.flask_server = Flask(__name__)
            self.socketio = SocketIO(self.flask_server, async_mode=None)
            self.flask_server.route(self.index_namespace,  methods=['GET', 'POST'])(page_index)
            self.socketio.on('get_dev_status', namespace=self.index_namespace)(self.get_dev_status)
            self.socketio.on('disconnect_request', namespace=self.index_namespace)(self.disconnect_request)
            self.flask_server.route(self.graph_namespace, methods=['GET', 'POST'])(page_graph)
            self.socketio.on('connect', namespace=self.graph_namespace)(self.socketio_on_connect)
            self.socketio.on('disconnect_request', namespace=self.graph_namespace)(self.disconnect_request)
            self.socketio.on('start_sdr', namespace=self.graph_namespace)(self.start_sdr)
            self.socketio.on('stop_sdr', namespace=self.graph_namespace)(self.stop_sdr)
            self.socketio.on('restart_sdr', namespace=self.graph_namespace)(self.restart_sdr)
            self.socketio.on('start_scan', namespace=self.graph_namespace)(self.start_scan)
            self.socketio.on('send_cli_args', namespace=self.graph_namespace)(self.send_cli_args)
            self.socketio.on('update_settings', namespace=self.graph_namespace)(self.update_settings)
            self.socketio.on('server_ping', namespace=self.graph_namespace)(self.server_ping)
            self.flask_server.route(self.app_namespace)(page_app)
            self.socketio.on('send_app_args', namespace=self.app_namespace)(self.send_app_args))
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
            self.disconnect_request()
        except Exception as e:
            self.logcl.log("Failed to run Flask server.\n" + str(e), 'fatal')
            sys.exit()

    def get_dev_status(self):
        if not self.rtl_sdr.dev_open:
            if(self.rtl_sdr.init_device(init_dev=False, show_log=False)):
                self.socketio.emit('dev_status', 1, namespace=self.index_namespace)
            else:
                self.socketio.emit('dev_status', 0, namespace=self.index_namespace)
        else:
            self.socketio.emit('dev_status', 1, namespace=self.index_namespace)

    def socketio_on_connect(self):
        self.socket_log("RTLion started.")
        
    def disconnect_request(self):
        if self.rtl_sdr.dev_open:
            self.rtl_sdr.close(True)
        self.logcl.log("Stopping server...")
        self.socketio.stop()

    def server_ping(self): 
        self.socketio.emit('server_pong', namespace=self.graph_namespace)

    def start_sdr(self, freq=None):
        if not self.rtl_sdr.dev_open:
            if(self.rtl_sdr.init_device()):
                self.socket_log("RTL-SDR device opened. [#" + str(self.rtl_sdr.dev_id) + "]")
                self.create_fft_graph(freq)
            else:
                self.socket_log("Failed to open RTL-SDR device. [#" + str(self.rtl_sdr.dev_id) + "]")
                self.socketio.emit('dev_status', 0, namespace=self.graph_namespace)
        else:
            self.create_fft_graph(freq)

    def stop_sdr(self):
        try:
            self.logcl.log("Stop reading samples from RTL-SDR.")
            self.socket_log("Stop reading samples from RTL-SDR.")
            self.socketio.emit('dev_status', 0, namespace=self.graph_namespace)
            self.c_read = False
            self.n_read = 0
        except Exception as e:
            self.logcl.log("Failed to stop RTL-SDR device.\n" + str(e), 'error')
            sys.exit()

    def restart_sdr(self, new_freq):
        try:
            self.c_read = False
            self.n_read = 0
            self.rtl_sdr.close()
            self.rtl_sdr.center_freq = int(new_freq)
            self.rtl_sdr.init_device(show_log=False)
            self.socketio.emit('new_freq_set', namespace=self.graph_namespace)
        except Exception as e:
            self.logcl.log("Failed to set new frequency.\n" + str(e), 'error')
            sys.exit()

    def start_scan(self, freq, sensivity):
        self.rtl_sdr.sensivity = sensivity
        self.rtl_sdr.close()
        self.rtl_sdr.center_freq = int(freq)
        self.start_sdr(freq=-1)

    def send_cli_args(self, status=0):
        self.socketio.emit(
                'cli_args', 
                {'args': self.rtl_sdr.args, 'status': status}, 
                namespace=self.graph_namespace)
            
    def send_app_args(self):
        self.socketio.emit(
            'cli_args', 
            {'args': self.rtl_sdr.args}, 
            namespace=self.app_namespace)

    def update_settings(self, args):
        try:
            self.rtl_sdr.set_args(args)
            self.send_cli_args(status=1)
            self.logcl.log("Settings/arguments updated.")
            self.socket_log("Settings/arguments updated.")
        except:
            self.logcl.log("Failed to update settings.", 'error')

    def update_app_settings(self, args):
        try:
            self.rtl_sdr.set_args(args)
            if self.rtl_sdr.dev_open:
                self.rtl_sdr.close()
                self.rtl_sdr.init_device(show_log=False)
            self.send_app_args()
        except:
            self.logcl.log("Failed to update settings.", 'error')

    def get_fft_graph(self):
        self.get_dev_status()
        self.socketio.emit(
            'fft_data', 
            {'data': self.rtl_sdr.get_fft_data()}, 
            namespace=self.app_namespace)

    def get_scanned_values(self, sensivity):
        self.get_dev_status()
        self.rtl_sdr.sensivity = int(sensivity)
        self.send_data_thread(ns=2, parse_json=True)
    
    def create_fft_graph(self, freq_change):
        self.n_read = self.rtl_sdr.num_read
        self.interval = int(self.rtl_sdr.interval) / 1000.0
        if freq_change == None:
            self.socketio.emit('dev_status', 1, namespace=self.graph_namespace)
            self.socket_log("Creating FFT graph from samples...")
            self.logcl.log("Creating FFT graph from samples...")
            self.logcl.log("Getting graph data with interval " + 
            str(self.interval) + " (" + str(self.n_read) + "x)")
        if freq_change != None and int(freq_change) == -1:
            self.socketio.emit('dev_status', 1, namespace=self.graph_namespace)
            self.socketio.start_background_task(self.send_data_thread)
        else:
            self.c_read = True
            self.socketio.start_background_task(self.rtlsdr_thread)

    def rtlsdr_thread(self):
        while self.c_read:
            fft_data = self.rtl_sdr.get_fft_data()
            self.socketio.emit(
            'fft_data', 
            {'data': fft_data},
            namespace=self.graph_namespace)
            self.socketio.sleep(self.interval)
            self.n_read-=1
            if self.n_read == 0: break
    
    def send_data_thread(self, ns=1, parse_json=False):
        graph_values = self.rtl_sdr.get_fft_data(scan=True)
        try:
            if not parse_json:
                self.socketio.emit(
                    'graph_data', 
                    {'fft': graph_values[0], 
                    'freqs': graph_values[1][0],
                    'dbs': graph_values[1][1]},
                    namespace=self.routes[ns])
            else:
                def get_str_from_list(lst):
                    try: 
                        return ' '.join(str(float(i)) for i in lst)
                    except: 
                        return None
                self.socketio.emit(
                    'graph_data', 
                    graph_values[0] + "|" + \
                    get_str_from_list(graph_values[1][0]) + "|" + \
                    get_str_from_list(graph_values[1][1]),
                    namespace=self.routes[ns])
        except:
            self.socketio.emit(
                    'graph_data', 
                    None,
                    namespace=self.routes[ns])

    def socket_log(self, msg):
        self.socketio.emit('log_message', {'msg': msg}, 
            namespace=self.graph_namespace)
