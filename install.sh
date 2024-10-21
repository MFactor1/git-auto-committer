#!/bin/sh

################################################################
#           INSTALL SCRIPT for git-auto-commiter (GAC)         #
#               Must be run as root (with sudo)                #
################################################################

USER=$(logname)
BIN_DIR="/usr/local/bin"
LIB_DIR="/usr/local/lib/gac"
CONF_DIR="/home/$USER/.config"
SERVICE_FILE="/usr/local/lib/gac/gac_daemon.service"
SERVICE_SYMLINK="/usr/lib/systemd/system/gac_daemon.service"

echo "Building source files"
./build.sh
echo "Copying backend files to $LIB_DIR/"
mkdir $LIB_DIR
cp build/*.pyc $LIB_DIR/
cp src/gacentry $LIB_DIR/gacentry
cp uninstall.sh $LIB_DIR/uninstall.sh
cp VERSION $LIB_DIR/VERSION
echo "Linking entrypoint to $BIN_DIR"
chmod +x $LIB_DIR/gacentry
ln -s $LIB_DIR/gacentry $BIN_DIR/gac
echo "Checking for ~/.config folder"
if [ ! -d $CONF_DIR ]; then
	echo "Creating ~/.config folder"
	mkdir $CONF_DIR
fi

echo "Writing service file to $SERVICE_FILE"
touch $SERVICE_FILE
cat <<EOF > $SERVICE_FILE
[Unit]
Description=git-auto-commiter (GAC) daemon
After=network.target

[Service]
ExecStart=/usr/bin/env python3 /usr/local/lib/gac/gacmain.pyc
Restart=always
User=$USER
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
echo "Linking service file to $SERVICE_SYMLINK"
ln -s $SERVICE_FILE $SERVICE_SYMLINK
echo "Reloading daemons"
systemctl daemon-reload
echo "Install Complete"
