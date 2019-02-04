#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from rtlcat.rtldev import RTLSdr
from rtlcat.argparser import parse_cli_args


def main():

    rtl_sdr = RTLSdr(**parse_cli_args())
    rtl_sdr.create_graph(True, 100)
    rtl_sdr.close()

if __name__ == "__main__":
    main()