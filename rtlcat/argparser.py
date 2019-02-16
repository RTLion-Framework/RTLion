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
                        help="center frequency (Hz)")

    parser.add_argument("-g",
                        "--gain",
                        help="gain (0 for auto) (default: ~1-3)")

    args = vars(parser.parse_args())
    return args