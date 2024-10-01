import gevent
from gevent.event import Event
from gaccmd import check_diff, commit_all

class Worker():
    def __init__(self, path: str, interval: int):
        self.path = path
        self.interval = interval
        self.stop = Event()

    def main_loop(self):
        if check_diff(self.path):
            commit_all(self.path)

        if self.stop.wait(timeout=60 * self.interval):
            return

    def start(self):
        self.instance = gevent.spawn(self.main_loop)

    def stop(self):
        self.stop.set()
        self.instance.join(timeout=10)

