#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from scripts.rtlhandler import rtl_sdr

def main():
    rtl_sdr().open_device()
    
if __name__ == "__main__":
    main()