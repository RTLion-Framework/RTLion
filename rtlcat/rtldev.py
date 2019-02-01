#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys

class RTLSdr:
    def __init__(self, **args):
        self.default_device_id = 0
        self.default_sample_rate = 2.048e6
        self.default_gain = 0
        self.dev_id = args['dev'] if args['dev'] else default_device_id
        self.sample_rate = args['samprate'] if args['samprate'] else default_sample_rate
        self.gain = args['gain'] if args['gain'] else default_gain
        self.center_freq = args['freq']
        self.no_colors = args['nocolors']
        self.filename = args['filename']
        self.import_rtlsdr()
    
    def import_rtlsdr(self):
        try:
            global RtlSdr
            from rtlsdr import RtlSdr
        except:
            print("rtlsdr module not found.")
            sys.exit()

    def open_device(self):
        try:
            rtl_sdr = RtlSdr()
        except IOError as e:
            print("Failed to open RTL-SDR device.\n" + str(e))
            sys.exit()