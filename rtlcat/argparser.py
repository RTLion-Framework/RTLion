#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import argparse

def parse_cli_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d",
                        "--dev",
                        help="device index (default: 0)",
                        default=0)

    parser.add_argument("-s",
                        "--samprate",
                        help="sample rate (default: 2048000 Hz)",
                        default=2048000)

    parser.add_argument("-f",
                        "--freq",
                        help="center frequency (Hz)")

    parser.add_argument("-g",
                        "--gain",
                        help="gain (0 for auto) (default: ~1-3)",
                        default="auto")

    parser.add_argument("host:port", nargs='?',
                        help="IP address/hostname and port number " 
                        "for server to listen on (default: 0.0.0.0:8081)",
                        default="0.0.0.0:8081")

    args = vars(parser.parse_args())
    return args