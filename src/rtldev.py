#!/usr/bin/python3.7
# -*- coding: utf-8 -*-

import sys
import os
import base64
import math
from src.logcl import LogCL

class RTLSdr:
    def __init__(self, **args):
        self.logcl = LogCL()
        self.import_rtlsdr()
        self.import_pylab()
        self.set_static_dir()
        self.set_args(args)
        self.dev = None
        self.dev_open = False
        self.sensivity = 3
        self.stop_func = None

    def set_static_dir(self):
        full_path = os.path.realpath(__file__)
        self.static_dir = os.path.split(full_path)[0] + '/static/'

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
    
    def import_pylab(self):
        try:
            global plt, np, peakutils
            import pylab as plt
            import numpy as np
            import peakutils
        except Exception as e:
            if 'peak' in str(e):
                self.logcl.log("peakutils module not found.\n" + str(e), 'error')
            else:
                self.logcl.log("matplotlib module not found.\n" + str(e), 'error')
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
            if not self.dev.device_opened:
                if not self.stop_func == None:
                    self.dev_open = False
                    self.stop_func()
            else:
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
            
    def find_peaks(self, plt, Y, F, n):
        try:
            freqs = []
            dbs = []
            indexes = peakutils.indexes(Y, thres=abs(11-(n))/10, min_dist=20)
            for index in indexes:
                freq = F[index]
                db = 10 * math.log10(Y[index])
                freqs.append(freq)
                dbs.append(db)
                plt.plot(freq, db, 
                    color='k', 
                    marker='x', 
                    markersize=6, 
                    linestyle='None')
            return [freqs, dbs]
        except:
            self.logcl.log("Failed to find peaks on graph.\n" + str(e), 'error')

    def get_fft_data(self, scan=False):
        try:
            [Y, F] = plt.psd(self.read_samples(), NFFT=1024, Fs=int(self.sample_rate)/1e6, \
                    Fc=int(self.center_freq)/1e6, color='k')    
            if scan: max_freqs = self.find_peaks(plt, Y, F, n=self.sensivity)
            plt.xlabel('Frequency (MHz)')
            plt.ylabel('Relative power (dB)')
            plt.savefig(self.static_dir + '/img/fft.png', bbox_inches='tight', pad_inches = 0)
            plt.clf()
            encoded = base64.b64encode(open(self.static_dir + '/img/fft.png', "rb"). \
                    read()).decode("utf-8")
            return encoded if not scan else [encoded, max_freqs]
        except Exception as e:
            self.logcl.log("Failed to get graph data.\n" + str(e), 'error')
