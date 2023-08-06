from unittest import TestCase
from zeroinger.time.stopwatch import StopWatch
import time


class TestStopWatch(TestCase):
    timer = StopWatch.create_instance()
    time.sleep(1)
    print(timer.snapshot())
    time.sleep(1)
    print(timer.duriation())
    timer.reset()
    time.sleep(1)
    print(timer.duriation())
    pass
