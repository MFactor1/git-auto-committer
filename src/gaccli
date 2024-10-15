#!/usr/bin/env python3
import argparse
import subprocess
import os

try:
    import gevent
except ImportError:
    print("gac requires gevent to be installed.\nTry: `pip install gevent`")
    exit(1)

home = os.path.expanduser('~')
repofile = f"{home}/.config/gac/repos"

def add(name: str, path: str, interval: int) -> bool:
    if not is_active():
        print("WARNING: GAC daemon not running, changes will save, but not take effect until it is running.")
        print("Hint: you can start the GAC daemon with `gac start`")

    if not os.path.exists(os.path.dirname(repofile)):
        os.makedirs(os.path.dirname(repofile))

    if os.path.exists(repofile):
        with open(repofile, "r") as f:
            repo_names = [repo.split(",")[0].strip() for repo in f.readlines()]
            if name in repo_names:
                print(f"A tracked repository with name '{name}' already exists")
                return False

    with open(repofile, "a") as f:
        f.write(f"{name},{path},{interval}\n")

    print(f"Started tracking repo {name} every {interval} minutes at {path}")
    return True

def remove(name: str) -> bool:
    if not is_active():
        print("WARNING: GAC daemon not running, changes will save, but not take effect until it is running.")
        print("Hint: you can start the GAC daemon with `gac start`")

    if not os.path.exists(repofile):
        print(f"Repo '{name}' does not exist")
        return False

    with open(repofile, "r") as f:
        repos = f.readlines()

    new_repos = []
    for repo in repos:
        if repo.split(",")[0].strip() != name:
            new_repos.append(repo)

    if len(repos) == len(new_repos):
        print(f"Repo '{name}' does not exist")
        return False

    with open(repofile, "w") as f:
        f.writelines(new_repos)

    print(f"Stopped tracking repo with name {name}")
    return True

def list(machine: bool) -> bool:
    err = False
    if not os.path.exists(repofile):
        return True

    with open(repofile, "r") as f:
        repos = f.readlines()

    for repo in repos:
        vals = [val.strip() for val in repo.split(',')]
        if len(vals) != 3:
            print(f"Malformed Entry: {vals}")
            err = True
            continue
        if machine:
            print(f"{vals[0]} {vals[2]} {vals[1]}")
        else:
            print(f"Name: {vals[0]}, Interval: {vals[2]} min, Path: {vals[1]}")

    if err:
        return False
    return True

def start() -> bool:
    try:
        if is_active():
            print(f"GAC daemon already running")
            return False

        subprocess.run(["sudo", "systemctl", "start", "gac_daemon.service"], capture_output=True, text=True, check=True)
        print(f"Started GAC daemon")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: failed to start GAC daemon: {e.stderr}")
        return False

def stop() -> bool:
    try:
        if not is_active():
            print(f"GAC daemon is not running")
            return False

        subprocess.run(["sudo", "systemctl", "stop", "gac_daemon.service"], capture_output=True, text=True, check=True)
        print(f"Stopped GAC daemon")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: failed stop GAC daemon: {e.stderr}")
        return False

def status() -> bool:
    try:
        active = is_active(passthrough=True)
        enabled = is_enabled(passthrough=True)
        print(f"GAC daemon - {active}, {enabled}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error: failed to get GAC daemon status: {e.stderr}")
        return False

def enable() -> bool:
    try:
        if is_enabled():
            print("GAC daemon is already enabled")
            return False

        subprocess.run(['sudo', 'systemctl', 'enable', 'gac_daemon.service'], capture_output=True, text=True, check=True)
        print("GAC daemon enabled")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error: failed to enable GAC daemon: {e.stderr}")
        return False

def disable() -> bool:
    try:
        if not is_enabled():
            print("GAC daemon is already disabled")
            return False

        subprocess.run(['sudo', 'systemctl', 'disable', 'gac_daemon.service'], capture_output=True, text=True, check=True)
        print("GAC daemon disabled")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error: failed to disable GAC daemon: {e.stderr}")
        return False

def is_enabled(passthrough=False):
    result = subprocess.run(['systemctl', 'is-enabled', 'gac_daemon.service'], capture_output=True, text=True, check=False)
    if passthrough:
        return result.stdout.strip()

    if result.stdout.strip() == "enabled" or result.stdout.strip() == "indirect":
        return True
    else:
        return False

def is_active(passthrough=False):
    result = subprocess.run(['systemctl', 'is-active', 'gac_daemon.service'], capture_output=True, text=True, check=False)
    if passthrough:
        return result.stdout.strip()

    if result.stdout.strip() == "active":
        return True
    else:
        return False

def main():
    with open("/usr/local/lib/gac/VERSION", "r") as f:
        VERSION = f.readline().strip()

    parser = argparse.ArgumentParser(description='git-auto-commiter (GAC) CLI')
    parser.add_argument('-v', '--version', action='version', version=f'git-auto-commiter (GAC), Version {VERSION}', help='prints the version information')
    subparsers = parser.add_subparsers(dest='action', help='available actions')

    parser_add = subparsers.add_parser('add', help='add a repo to be tracked')
    parser_add.add_argument("name", type=str, help="unique name of tracker entry")
    parser_add.add_argument("interval", type=int, help="how often in minues to check the given repo")
    parser_add.add_argument("path", type=str, help="path of top level directory of desired repo")

    parser_rm = subparsers.add_parser('remove', help='remove a tracked repo by name')
    parser_rm.add_argument('name', type=str, help="name of tracked repo to remove")

    parser_list = subparsers.add_parser('list', help='lists all tracked repos')
    parser_list.add_argument('-m', action='store_true', help="formats the output to be easier to parse for scripts")

    subparsers.add_parser('start', help='starts the GAC daemon')

    subparsers.add_parser('stop', help='stops the GAC daemon')

    subparsers.add_parser('enable', help='enable run on startup for GAC daemon')

    subparsers.add_parser('disable', help='disable run on startup for GAC daemon')

    subparsers.add_parser('status', help='gets the status of the GAC daemon')

    args = parser.parse_args()

    if args.action == 'add':
        success = add(args.name, args.path, args.interval)
    elif args.action == 'remove':
        success = remove(args.name)
    elif args.action == 'list':
        success = list(args.m)
    elif args.action == 'start':
        success = start()
    elif args.action == 'stop':
        success = stop()
    elif args.action == 'enable':
        success = enable()
    elif args.action == 'disable':
        success = disable()
    elif args.action == 'status':
        success = status()
    else:
        parser.print_help()
        success = False

    if success:
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()
