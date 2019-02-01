#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import sys

class rtl_sdr:
    def __init__(self):
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