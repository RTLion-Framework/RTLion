#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys

class RTLSdr:
    def __init__(self, **args):
        self.import_rtlsdr()
        self.default_device_id = 0
        self.default_sample_rate = 2.048e6
        self.default_gain = 'auto'
        self.dev_id = args['dev'] if args['dev'] else self.default_device_id
        self.sample_rate = args['samprate'] if args['samprate'] \
                                            else self.default_sample_rate
        self.gain = int(args['gain']) if args['gain'] else self.default_gain
        self.center_freq = args['freq']
        self.no_colors = args['nocolors']
        self.filename = args['filename']
        self.dev = None
        self.open_device()
        self.initialize_device()
    
    def import_rtlsdr(self):
        try:
            global RtlSdr
            from rtlsdr import RtlSdr
        except:
            print("rtlsdr module not found.")
            sys.exit()

    def open_device(self):
        try:
            self.dev = RtlSdr(self.dev_id)
        except IOError as e:
            print("Failed to open RTL-SDR device.\n" + str(e))
            sys.exit()

    def initialize_device(self):
        try:
            self.dev.sample_rate = self.sample_rate
            self.dev.center_freq = self.center_freq
            self.dev.gain = self.gain
        except Exception as e:
            print("Failed to initialize RTL-SDR device.\n" + str(e))
            sys.exit()

            