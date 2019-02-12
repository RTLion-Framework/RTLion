#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from rtlcat.rtlserver import FlaskServer
from rtlcat.argparser import parse_cli_args

def main():

    flask_server = FlaskServer(**parse_cli_args())
    flask_server.run()
    
if __name__ == "__main__":
    main()