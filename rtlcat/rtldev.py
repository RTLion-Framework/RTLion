#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
import os
import base64

class RTLSdr:
    def __init__(self, **args):
        self.import_rtlsdr()
        self.default_device_id = 0
        self.default_sample_rate = 2.048e6
        self.default_gain = 'auto'
        self.set_args(args)
        self.dev = None
        self.static_dir = 'rtlcat/static/'
        self.create_static_dir()

    def set_args(self, args):
        self.dev_id = args['dev'] if args['dev'] else self.default_device_id
        self.sample_rate = args['samprate'] if args['samprate'] \
                                            else self.default_sample_rate
        self.gain = args['gain'] if args['gain'] else self.default_gain
        self.center_freq = args['freq']
        self.args = {
            'freq': self.center_freq, 
            'samprate': self.sample_rate, 
            'dev': self.dev_id, 
            'gain': self.gain}

    def create_static_dir(self):
        try:
            if not os.path.exists(self.static_dir):
                os.makedirs(self.static_dir)
        except Exception as e:
            print("Failed to create static directory.\n" + str(e))
            sys.exit()
    
    def import_rtlsdr(self):
        try:
            global RtlSdr
            from rtlsdr import RtlSdr
        except:
            print("rtlsdr module not found.")
            sys.exit()

    def init_device(self):
        try:
            self.dev = RtlSdr(self.dev_id)
        except IOError as e:
            # Warning
            print("Failed to open RTL-SDR device!\n" + str(e))
        try:
            self.dev.center_freq = self.center_freq
            self.dev.sample_rate = self.sample_rate
            self.dev.gain = self.gain
        except Exception as e:
            # Warning
            print("Failed to initialize RTL-SDR device.")

    def read_samples(self, n_read=512*512):
        try:
            return self.dev.read_samples(n_read)
        except Exception as e:
            print("Failed to read samples from RTL-SDR.\n" + str(e))

    def close(self):
        try:
            self.dev.close()
        except Exception as e:
            print("Failed to close RTL-SDR device.\n" + str(e))

    def create_graph(self, continous=False, read_count=1, refresh_rate=0.05):
        try:
            from pylab import psd, xlabel, ylabel, pause, clf, show
            for i in range(read_count):
                psd(self.read_samples(), NFFT=1024, Fs=int(self.sample_rate)/1e6, \
                    Fc=int(self.center_freq)/1e6)
                xlabel('Frequency (MHz)')
                ylabel('Relative power (dB)')
                if continous:
                    pause(refresh_rate)
                    clf()
                else: show()
        except Exception as e:
            print("Failed to create graph.\n" + str(e))
    
    def get_fft_data(self):
        try:
            from pylab import psd, xlabel, ylabel, title, clf, savefig
            fft_plot = psd(self.read_samples(), NFFT=1024, Fs=int(self.sample_rate)/1e6, \
                    Fc=int(self.center_freq)/1e6)
            title("rtl_cat")
            xlabel('Frequency (MHz)')
            ylabel('Relative power (dB)')
            savefig(self.static_dir + '/fft.png', bbox_inches='tight')
            clf()
            encoded = base64.b64encode(open(self.static_dir + '/fft.png', "rb").read())
            return encoded
        except Exception as e:
            print("Failed to get graph data.\n" + str(e))
