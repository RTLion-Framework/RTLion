#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
import base64

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

    def read_samples(self, n_read=512*512):
        try:
            return self.dev.read_samples(n_read)
        except Exception as e:
            print("Failed to read samples from RTL-SDR.\n" + str(e))
            sys.exit()

    def close(self):
        try:
            self.dev.close()
        except Exception as e:
            print("Failed to close RTL-SDR device.\n" + str(e))
            sys.exit()

    def create_graph(self, continous=False, read_count=1, refresh_rate=0.05):
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
    
    def get_fft_data(self):
        from pylab import psd, xlabel, ylabel, title, clf, savefig
        fft_plot = psd(self.read_samples(), NFFT=1024, Fs=int(self.sample_rate)/1e6, \
                Fc=int(self.center_freq)/1e6)
        title("rtl_cat")
        xlabel('Frequency (MHz)')
        ylabel('Relative power (dB)')
        savefig('rtlcat/static/fft.png', bbox_inches='tight')
        clf()
        encoded = base64.b64encode(open("rtlcat/static/fft.png", "rb").read())
        return encoded
