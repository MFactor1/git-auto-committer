import os
from gevent import sleep
from gacworker import Worker

def new_worker(path: str, interval: int) -> Worker:
    worker = Worker(path, interval)
    worker.start()
    return worker

def stop_worker(key):
    worker = repos.pop(key)
    worker.stop()

repos = dict()
home = os.path.expanduser('~')
repofile = f"{home}/.config/gac/repos"

while True:
    workers_to_stop = []
    if not os.path.exists(os.path.dirname(repofile)):
        os.makedirs(os.path.dirname(repofile))

    if not os.path.exists(repofile):
        with open(repofile, "w"):
            pass

    with open(repofile, "r") as f:
        file_repos = f.readlines()
        for repo in file_repos:
            if repo != '' and repo not in repos:
                repos[repo] = new_worker(repo.split(',')[1], int(repo.split(',')[2]))

        for repo_key in repos.keys():
            if repo_key not in file_repos:
                workers_to_stop.append(repo_key)

        for key in workers_to_stop:
            stop_worker(key)

    sleep(1)
