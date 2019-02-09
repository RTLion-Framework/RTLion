#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from rtlcat.rtldev import RTLSdr
from rtlcat.rtlserver import FlaskServer
from rtlcat.argparser import parse_cli_args

def main():

    flask_server = FlaskServer()
    flask_server.run()

    #rtl_sdr = RTLSdr(**parse_cli_args())
    #rtl_sdr.create_graph(True, 100)
    #rtl_sdr.close()
1
if __name__ == "__main__":
    main()