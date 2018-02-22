import time

class TimeHelper(object):
    def __init__(self):
        pass

    @staticmethod
    def formatTime1():
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))