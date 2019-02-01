#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from rtlcat.rtldev import RTLSdr

def main():
    RTLSdr().open_device()
    
if __name__ == "__main__":
    main()