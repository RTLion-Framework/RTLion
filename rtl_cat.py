#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from rtlcat.rtldev import RTLSdr
from rtlcat.argparser import parse_cli_args

def main():
    
    rtl_sdr = RTLSdr(**parse_cli_args())
    samples = rtl_sdr.read_samples()
    rtl_sdr.close()

    print(samples)

if __name__ == "__main__":
    main()