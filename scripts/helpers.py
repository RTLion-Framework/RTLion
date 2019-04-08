#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import argparse
from logcl import LogCL

def print_start_msg():
    g_attr = LogCL().attr_gray
    g_attr_off = LogCL().attr_gray_off
    ascii_logo = LogCL().bold_attr + \
    LogCL().color_lwhite + \
    """                             
                 :       .      
                  :      `.       | RTLion Framework | 
                  .-      -      """ + g_attr + """ Multipurpose RTL-SDR Framework.""" + g_attr_off + """
                   -`     -      """ + g_attr + """ Created for RTL2832 based DVB-T receivers.""" + g_attr_off + """
                    /     `-     """ + g_attr + """ https://github.com/RTLion-Framework""" + g_attr_off + """
                    `/     :     """ + g_attr + """ Copyright (C) 2019 by KeyLo99""" + g_attr_off + """
                     .:    :     
.`      ``            :.   `: 
 `...    `..         .:o-.  /
    `--.    ..    `sNdh+-++::`
       `--.   .-`.ms-+dNmyMMm:
          `---  .y+oNMMMMhMMMo
             `-:-.+MMMMMMMMMM:
                `:oMMMMMMMmN+ 
                   .+RTLion/`
    """ + LogCL().all_attr_off
    print(ascii_logo)

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

    parser.add_argument("-n",
                        "-num",
                        help="number of the reads (default: -1, inf.)",
                        default=-1)
    
    parser.add_argument("-i",
                        "-interval",
                        help="interval between reads (default: 500ms)",
                        default=500)

    parser.add_argument("host:port", nargs='?',
                        help="IP address/hostname and port number " 
                        "for server to listen on (default: 0.0.0.0:8081)",
                        default="0.0.0.0:8081")

    args = vars(parser.parse_args())
    LogCL().log("Starting...")
    return args
