import gevent
from gevent.event import Event
from gaccmd import check_diff, commit_all

class Worker():
    def __init__(self, path: str, interval: int):
        self.path = path
        self.interval = interval
        self.stop_sig = Event()

    def main_loop(self):
        while True:
            if check_diff(self.path):
                print(f"diff exists for {self.path}, commiting")
                commit_all(self.path)
            else:
                print(f"no diff for {self.path}, skipping")

            if self.stop_sig.wait(timeout= 60 * self.interval):
                print("returning on stop() command")
                return

    def start(self):
        self.instance = gevent.spawn(self.main_loop)

    def stop(self):
        self.stop_sig.set()
        self.instance.join(timeout=10)

