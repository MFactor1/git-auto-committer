import argparse
import subprocess
import os

home = os.path.expanduser('~')
repofile = f"{home}/.config/gac/repos"

def add(name: str, path: str, interval: int) -> bool:
    gac_running = subprocess.check_output(['systemctl', 'is-active', 'gac_daemon.service'])
    if gac_running == "inactive":
        print("WARNING: GAC daemon not running, changes will save, but not take effect until it is running.")
        print("Hint: you can start the GAC daemon with `gac start`")

    if not os.path.exists(os.path.dirname(repofile)):
        os.makedirs(os.path.dirname(repofile))

    if os.path.exists(repofile):
        with open(repofile, "r") as f:
            repo_names = [repo.split(",")[0] for repo in f.readlines()]
            if name in repo_names:
                print(f"A tracked repository with name '{name}' already exists")
                return False

    with open(repofile, "a") as f:
        f.write(f"{name},{path},{interval}\n")

    return True

def remove(name: str) -> bool:
    gac_running = subprocess.check_output(['systemctl', 'is-active', 'gac_daemon.service'])
    if gac_running == "inactive":
        print("WARNING: GAC daemon not running, changes will save, but not take effect until it is running.")
        print("Hint: you can start the GAC daemon with `gac start`")

    if not os.path.exists(repofile):
        print(f"Repo '{name}' does not exist")
        return False

    with open(repofile, "r") as f:
        repos = f.readlines()

    new_repos = []
    for repo in repos:
        if repo.split(",")[0] != name:
            new_repos.append(repo)

    if len(repos) == len(new_repos):
        print(f"Repo '{name}' does not exist")
        return False

    with open(repofile, "w") as f:
        f.writelines(new_repos)

    return True

def list(machine: bool) -> bool:
    if not os.path.exists(repofile):
        return True

    with open(repofile, "r") as f:
        repos = f.readlines()

    for repo in repos:
        vals = repo.split(',')
        if machine:
            print(f"{vals[0]} {vals[2]} {vals[1]}")
        else:
            print(f"Name: {vals[0]}, Interval: {vals[2]}min, Path: {vals[1]}")

    return True

def start() -> bool:
    try:
        result = subprocess.check_output(["systemctl", "is-active", "gac_daemon.service"])
        if result.strip() == "active":
            print(f"GAC deamon already running")
            return False

        subprocess.run(["systemctl", "start", "gac_daemon.service"], capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: failed to start GAC daemon: {e.stderr}")
        return False

def stop() -> bool:
    try:
        result = subprocess.check_output(["systemctl", "is-active", "gac_daemon.service"])
        if result.strip() == "inactive":
            print(f"GAC deamon is not running")
            return False

        subprocess.run(["systemctl", "stop", "gac_daemon.service"], capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: failed stop GAC daemon: {e.stderr}")
        return False

def status() -> bool:
    try:
        result = subprocess.check_output(["systemctl", "is-active", "gac_daemon.service"])
        if result.strip() == "active":
            print(f"GAC deamon is running")
        else:
            print(f"GAC deamon is not running")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error: failed to get GAC daemon status: {e.stderr}")
        return False

parser = argparse.ArgumentParser(description='git auto commit commandline')
subparsers = parser.add_subparsers(dest='action', help='Available actions')

parser_add = subparsers.add_parser('add', help='Add a repo to be tracked')
parser_add.add_argument("name", type=str, help="Unique name of tracker entry")
parser_add.add_argument("interval", type=int, help="How often in minues to check the given repo")
parser_add.add_argument("path", type=str, help="Path of top level directory of desired repo")

parser_rm = subparsers.add_parser('remove', help='Remove a tracked repo by name')
parser_add.add_argument('name', type=str, help="Name of tracked repo to remove")

parser_list = subparsers.add_parser('list', help='Lists all tracked repos')
parser_list.add_argument('-m', action='store_true', help="Formats the output to be easier to parse for scripts")

parser_start = subparsers.add_parser('start', help='starts the GAC daemon')

parser_stop = subparsers.add_parser('stop', help='stops the GAC daemon')

parser_status = subparsers.add_parser('status', help='gets the status of the GAC daemon')

args = parser.parse_args()

if args.action == 'add':
    add_args = parser_add.parse_args()
    add(add_args.name, add_args.path, add_args.interval)
elif args.action == 'remove':
    remove_args = parser_rm.parse_args()
    remove(remove_args.name)
elif args.action == 'list':
    list_args = parser_list.parse_args()
    list(list_args.m)
elif args.action == 'start':
    start()
elif args.action == 'stop':
    stop()
elif args.action == 'status':
    status()
else:
    parser.print_help()
