#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
import os
import base64
from logcl import LogCL

class RTLSdr:
    def __init__(self, **args):
        self.logcl = LogCL()
        self.import_rtlsdr()
        self.set_args(args)
        self.dev = None
        self.dev_open = False
        self.static_dir = 'scripts/static/'

    def set_args(self, args):
        try:
            self.dev_id = int(args['dev'])
            self.sample_rate = int(args['samprate'])
            self.gain = args['gain']
            self.center_freq = args['freq']
            self.num_read = int(args['n'])
            self.interval = int(args['i'])
            self.args = args
        except Exception as e:
            self.logcl.log("Invalid argument detected.\n" + str(e), 'error')
            sys.exit()
    
    def import_rtlsdr(self):
        try:
            self.logcl.log("Importing rtlsdr module...")
            global RtlSdr
            from rtlsdr import RtlSdr
        except:
            self.logcl.log("rtlsdr module not found.", "error")
            sys.exit()

    def init_device(self, init_dev=True, show_log=True):
        try:
            if show_log: 
                self.logcl.log("Trying to open & initialize device #" + str(self.dev_id))
            self.dev = RtlSdr(self.dev_id)
            self.dev_open = True
            if init_dev:
                self.dev.center_freq = self.center_freq
                self.dev.sample_rate = self.sample_rate
                self.dev.gain = self.gain
        except IOError as e:
            self.dev_open = False
            if init_dev:
                self.logcl.log("Failed to open RTL-SDR device!\n" + str(e), 'error')
        except Exception as e:
            self.logcl.log("Failed to initialize RTL-SDR device.\n" + str(e), 'fatal')
        return self.dev_open

    def read_samples(self, n_read=512*512):
        try:
            return self.dev.read_samples(n_read)
        except Exception as e:
            self.logcl.log("Failed to read samples from RTL-SDR.\n" + str(e), 'error')

    def close(self, show_log=False):
        try:
            if show_log:
                self.logcl.log("Closing RTL-SDR device #" + str(self.dev_id))
            if self.dev != None:
                self.dev.close()
                self.dev_open = False
        except Exception as e:
            self.logcl.log("Failed to close RTL-SDR device.\n" + str(e), 'error')

    def create_graph(self, continous=False, read_count=1, refresh_rate=0.05):
        self.logcl.log("Creating graph...")
        try:
            from pylab import psd, xlabel, ylabel, pause, clf, show
            for i in range(read_count):
                psd(self.read_samples(), NFFT=1024, Fs=int(self.sample_rate)/1e6, \
                    Fc=int(self.center_freq)/1e6, color='k')
                xlabel('Frequency (MHz)')
                ylabel('Relative power (dB)')
                if continous:
                    pause(refresh_rate)
                    clf()
                else: show()
        except Exception as e:
            self.logcl.log("Failed to create graph.\n" + str(e), 'error')

    def get_fft_data(self, scan=False):
        try:
            from pylab import psd, xlabel, ylabel, title, clf, savefig
            [Y, F] = psd(self.read_samples(), NFFT=1024, Fs=int(self.sample_rate)/1e6, \
                    Fc=int(self.center_freq)/1e6, color='k')
            xlabel('Frequency (MHz)')
            ylabel('Relative power (dB)')
            savefig(self.static_dir + '/img/fft.png', bbox_inches='tight', pad_inches = 0)
            clf()
            encoded = base64.b64encode(open(self.static_dir + '/img/fft.png', "rb").read())
            return encoded
        except Exception as e:
            self.logcl.log("Failed to get graph data.\n" + str(e), 'error')
