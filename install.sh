#!/bin/sh
chmod +x src/gaccli.py
cp src/gaccli.py /usr/local/bin/gac
cp src/gac_daemon.service /etc/systemd/system/gac_daemon.service
systemctl daemon-reload
