#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from rtlcat.rtldev import RTLSdr
from rtlcat.argparser import parse_cli_args

def main():
    parse_cli_args()
    RTLSdr().open_device()
    
if __name__ == "__main__":
    main()