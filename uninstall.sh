#!/bin/sh

################################################################
#         UNINSTALL SCRIPT for git-auto-commiter  GAC         #
#               Must be run as root  with sudo                #
# For clean uninstall, manually remove /home/$USER/.config/gac #
################################################################

echo 'Stopping GAC daemon'
systemctl stop gac_daemon.service

echo 'Removing gac cli from /usr/local/bin/gac'
rm -f /usr/local/bin/gac
echo 'Removing service file /usr/lib/systemd/system/gac_daemon.service'
rm -f /usr/lib/systemd/system/gac_daemon.service
echo 'Removing backend files /usr/local/lib/gac/'
rm -rf /usr/local/lib/gac
echo 'Reloading daemons'
systemctl daemon-reload
echo 'Uninstall complete'
