#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
import json

class RTLNs:
    def __init__(self, socketio, rtl_sdr, logcl):
        self.socketio = socketio
        self.rtl_sdr = rtl_sdr
        self.logcl = logcl
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

    def get_routes(self):
        return self.routes

    def add_namespace(self, ns, methods):
        for method in methods:
             self.socketio.on(method, namespace=self.routes[ns])(getattr(self, method))

    def get_dev_status(self):
        if not self.rtl_sdr.dev_open:
            if(self.rtl_sdr.init_device(init_dev=False, show_log=False)):
                self.socketio.emit('dev_status', 1, namespace=self.index_namespace)
            else:
                self.socketio.emit('dev_status', 0, namespace=self.index_namespace)
        else:
            self.socketio.emit('dev_status', 1, namespace=self.index_namespace)

    def disconnect_request(self):
        if self.rtl_sdr.dev_open:
            self.rtl_sdr.close(True)
        self.logcl.log("Stopping server...")
        self.socketio.stop()