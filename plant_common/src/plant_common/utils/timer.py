from threading import Timer as ThreadingTimer


class Timer:

    def __init__(self, wait_time_s, function, args=None, kwargs=None):
        self._wait_time = wait_time_s
        self._function = function
        self._args = args
        self._kwargs = kwargs

        self._timer = None

    def start(self):
        self._timer = ThreadingTimer(
            self._wait_time, self._function, self._args, self._kwargs
        )
        self._timer.start()

    def reset(self):
        if self._timer:
            self._timer.cancel()
        self._timer = None

    def is_counting(self):
        if not self._timer:
            return False

        return not self._timer.finished.is_set()
