#!/bin/sh

################################################################
#         UNINSTALL SCRIPT for git-auto-commiter (GAC)         #
#               Must be run as root (with sudo)                #
# For clean uninstall, manually remove /home/$USER/.config/gac #
################################################################

systemctl stop gac_daemon.service

rm -f /usr/local/bin/gac
rm -f /etc/systemd/system/gac_daemon.service
rm -rf /usr/local/lib/gac
systemctl daemon-reload
