#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from rtlcat.rtldev import RTLSdr
from rtlcat.argparser import parse_cli_args
from pylab import *

def main():

    rtl_sdr = RTLSdr(**parse_cli_args())

    for i in range(50):
        samples = rtl_sdr.read_samples()
        psd(samples, NFFT=1024, Fs=int(rtl_sdr.sample_rate)/1e6, Fc=int(rtl_sdr.center_freq)/1e6)
        xlabel('Frequency (MHz)')
        ylabel('Relative power (dB)')
        pause(0.005)
        clf()

    rtl_sdr.close()

if __name__ == "__main__":
    main()