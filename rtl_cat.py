#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys

def import_rtlsdr():
    try:
        global RtlSdr
        from rtlsdr import RtlSdr
    except:
        print("rtlsdr module not found.")
        sys.exit()

def open_device():
    try:
        rtl_sdr = RtlSdr()
    except IOError as e:
        print("Failed to open RTL-SDR device.\n" + str(e))
        sys.exit()

def main():
    import_rtlsdr()
    open_device()
    
if __name__ == "__main__":
    main()