#!/bin/sh

################################################################
#           INSTALL SCRIPT for git-auto-commiter (GAC)         #
#               Must be run as root (with sudo)                #
################################################################

USER=$(logname)

cp src/gaccli /usr/local/bin/gac
mkdir /usr/local/lib/gac
cp src/*.py /usr/local/lib/gac/
cp uninstall.sh /usr/local/lib/gac/uninstall.sh
if [ ! -d /home/$USER/.config ]; then
	mkdir /home/$USER/.config
fi

SERVICE_FILE="/usr/local/lib/gac/gac_daemon.service"
touch $SERVICE_FILE
cat <<EOF > $SERVICE_FILE
[Unit]
Description=git-auto-commiter (GAC) daemon
After=network.target

[Service]
ExecStart=/usr/bin/env python3 /usr/local/lib/gac/gacmain.py
Restart=always
User=$USER
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
ln -s $SERVICE_FILE /etc/systemd/system/gac_daemon.service
systemctl daemon-reload

