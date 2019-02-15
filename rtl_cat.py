#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from rtlcat.rtlserver import FlaskServer
from rtlcat.rtldev import RTLSdr
from rtlcat.argparser import parse_cli_args

def main():

    rtl_sdr = RTLSdr(**parse_cli_args())
    flask_server = FlaskServer(rtl_sdr)
    flask_server.run()

if __name__ == "__main__":
    main()