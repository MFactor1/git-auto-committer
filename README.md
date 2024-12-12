# git-auto-commiter (GAC)
Students around the world use Git to manage academic projects, where frequent commits are often required to maintain academic integrity. git-auto-committer (GAC) is a CLI tool created by students, for students, to promote transparency throughout the academic process. GAC automates the creation of consistent, traceable, and reliable commits at scheduled intervals, allowing students to focus on their work without manual interruptions. By automatically committing on behalf of the user, GAC provides a clear record of project progress over time.

GAC gives students peace of mind, knowing they don’t need to worry about frequent manual commits, while instructors benefit from a detailed history of the students' work, readily available for review.
With the ability to track multiple repositories simultaneously each with their own commit schedule, GAC can handle all your projects at once, while only making new commits on the repositories that actually have changes.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
  - [Ubuntu/WSL](#ubuntuwsl)
  - [Fedora](#fedora)
  - [Others](#others)
- [Usage](#usage)

## Requirements
- A Linux or other UNIX-like system using systemd (WSL is supported)
- An installation of python >= 3.5
- An installation of the gevent python package (Try: `pip install gevent`)

## Installation
### Ubuntu/WSL
This method will install all dependencies automatically.

A `.deb` file is available in the "Releases" section.

Download the file and install it with:
```
sudo apt install <path to file>
```
For example, installing version `1.0.2` on Ubuntu/WSL:
```
sudo apt install ./git-auto-commiter-1.0.2_all.deb
```
You can check that the installation was sucessful by running `gac -v`, which should print the name and version.
### Fedora
This method will install all dependencies automatically.

A `.rpm` file is available in the "Releases" section to install via `dnf`.

Download the file and install it with:
```
sudo dnf install <path to file>
```
For example, installing version `1.0.2` on Fedora 40:
```
sudo dnf install ./git-auto-commiter-1.0.2-1.fc40.noarch.rpm
```
You can check that the installation was sucessful by running `gac -v`, which should print the name and version.
### Others
Note: MacOS is not supported at this time

You can install from source via the install script.
Clone this repo, and run the install script with sudo:
``` sh
git clone git@github.com:MFactor1/git-auto-commiter.git
cd git-auto-commiter
sudo ./install
```

Similarily, uninstallation can be completed via the uninstall script found in this repo:
``` sh
git clone git@github.com:MFactor1/git-auto-commiter.git
cd git-auto-commiter
sudo ./uninstall
```
You can check that the installation was sucessful by running `gac -v`, which should print the name and version.

Note: After installation, the cloned repo can be safely deleted. Hint: the uninstall script is placed in `/usr/local/lib/gac/` upon installation, so you can always find it there.

## Usage
- `gac add <name> <interval> <path>`: Adds tracker with name `<name>` with commit frequency of `<interval>` minutes, to repo at path `<path>`.
- `gac remove <name>`: Removes tracker with name `<name>`.
- `gac list [-m, --machine]`: Lists the all the active trackers. `-m` option produces a more script friendly output.
- `gac status`: Prints the status of the GAC daemon (active/inactive). GAC **requires** the GAC daemon to be **active** in order to create commits.
- `gac start`: Starts the GAC daemon.
- `gac stop`: Stops the GAC daemon.
- `gac enable`: Enables run on startup for the GAC daemon.
- `gac disable`: Disables run on startup for the GAC daemon.
- `gac -v, --version`: prints version information.
- `gac -h, --help`: prints a help message.
