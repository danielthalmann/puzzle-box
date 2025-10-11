
from datetime import timedelta
from datetime import datetime
import time


class Deltatime:

    last = time.time()

    @classmethod
    def tick(cls):
        return (time.time() - cls.last)

    @classmethod
    def update(cls):
        cls.last = time.time()

    @staticmethod
    def delta(days: float = 0,
                seconds: float = 0,
                microseconds: float = 0,
                milliseconds: float = 0,
                minutes: float = 0,
                hours: float = 0,
                weeks: float = 0):
        return timedelta(days,
                seconds,
                microseconds,
                milliseconds,
                minutes,
                hours,
                weeks)
         
    @staticmethod
    def isGreat(delta, milliseconds):
        
        limite = timedelta(milliseconds=milliseconds)
        if delta > limite:
            return True
        return False
