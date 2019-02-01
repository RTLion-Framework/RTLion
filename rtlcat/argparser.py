#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import argparse

def parse_cli_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d",
                        "--dev",
                        help="device index (default: 0)")

    parser.add_argument("-s",
                        "--samprate",
                        help="sample rate (default: 2048000 Hz)")

    parser.add_argument("-f",
                        "--freq",
                        help="center frequency (Hz)",
                        required=True)

    parser.add_argument("-g",
                        "--gain",
                        help="gain (0 for auto) (default: ~1-3)")

    parser.add_argument("-T",
                        "--nocolors",
                        action="store_true",
                        help="turn off log colors (default: on)")

    parser.add_argument("filename", nargs='?',
                        help="filename (a '-' dumps samples to stdout)")

    args = vars(parser.parse_args())
    return args