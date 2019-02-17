#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from rtlcat.rtlserver import FlaskServer
from rtlcat.rtldev import RTLSdr
from rtlcat.argparser import parse_cli_args

def main():

    cli_args = parse_cli_args()
    rtl_sdr = RTLSdr(**cli_args)
    flask_server = FlaskServer(rtl_sdr, cli_args['host:port'].split(':'))
    flask_server.run()

if __name__ == "__main__":
    main()