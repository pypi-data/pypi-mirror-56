import time
from pcommon.file import *


class Logger:
    filename = None

    def __init__(self, path):
        today = time.strftime("%Y-%m-%d", time.localtime())
        self.filename = path + '/' + today + '.log'

    def write(self, msg):
        File.write(self.filename, msg, True)

    def debug(self, msg):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        File.write(self.filename, '[' + now + '][DEBUG]\t' + str(msg) + '\n', True)

    def info(self, msg):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        File.write(self.filename, '[' + now + '][INFO]\t' + str(msg) + '\n', True)

    def error(self, msg):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        File.write(self.filename, '[' + now + '][ERROR]\t' + str(msg) + '\n', True)
