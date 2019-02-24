#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from scripts.rtlserver import FlaskServer
from scripts.rtldev import RTLSdr
from scripts.argparser import parse_cli_args
from scripts.logcl import LogCL

def start_message():
    LogCL().log("Starting...")

def main():
    start_message()
    cli_args = parse_cli_args()
    rtl_sdr = RTLSdr(**cli_args)
    flask_server = FlaskServer(rtl_sdr, cli_args['host:port'].split(':'))
    flask_server.run()

if __name__ == "__main__":
    main()