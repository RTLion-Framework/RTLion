#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from rtlcat.rtldev import RTLSdr
from rtlcat.argparser import parse_cli_args

def main():
    print(RTLSdr(**parse_cli_args()).read_samples())
    
if __name__ == "__main__":
    main()