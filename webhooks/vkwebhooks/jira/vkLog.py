#!/usr/bin/python
#coding:utf-8

import time

class Log():
    @staticmethod
    def tlog(log):
        local_time = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
        print " [ %s ] ** %s **" % (local_time, log)