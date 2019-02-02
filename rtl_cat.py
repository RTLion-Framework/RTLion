#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from rtlcat.rtldev import RTLSdr
from rtlcat.argparser import parse_cli_args

def main():
    RTLSdr(**parse_cli_args())
    
if __name__ == "__main__":
    main()