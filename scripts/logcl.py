#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import time

class LogCL:
    def __init__(self):
        self.levels = {
            'info': ('INFO', '\x1b[92m'),
            'error': ('ERROR', '\x1b[91m'),
            'fatal': ('FATAL', '\x1b[33m')}
        self.color_lwhite = "\x1b[97m"
        self.bold_attr = "\x1b[1m"
        self.attr_gray = "\x1b[21m\x1b[90m"
        self.attr_gray_off = "\x1b[97m" + self.bold_attr 
        self.all_attr_off = '\x1b[0m'
        
    def log(self, msg, level='info'):
        content = self.bold_attr + \
        "[" + time.strftime('%X') + "] " + \
        self.levels[level][1] + self.levels[level][0] + \
        self.all_attr_off + " " + msg
        print(content)