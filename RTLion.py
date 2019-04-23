#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from src.rtlserver import FlaskServer
from src.rtldev import RTLSdr
from src.helpers import *

def main():
    print_start_msg()
    cli_args = parse_cli_args()
    rtl_sdr = RTLSdr(**cli_args)
    flask_server = FlaskServer(rtl_sdr, 
        cli_args['host:port'].split(':'))
    flask_server.run()

if __name__ == "__main__":
    main()
