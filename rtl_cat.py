#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

def import_rtlsdr():
    try:
        global RtlSdr
        from rtlsdr import RtlSdr
    except ImportError as e:
        print("pyrtlsdr not found.")

def main():
    import_rtlsdr()
    rtl_sdr = RtlSdr()

if __name__ == "__main__":
    main()