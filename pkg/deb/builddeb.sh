#!/bin/bash

NAME=git-auto-commiter
VERSION=1.0.1
BLD_DIR=/home/$USER/$NAME-$VERSION-1_all
REPO_DIR=`dirname $0`/../../
DATA_DIR=/usr/share
BIN_DIR=/usr/bin
UNIT_DIR=/usr/lib/systemd/system/

$REPO_DIR/compile
rm -rf $BLD_DIR
mkdir -p $BLD_DIR/DEBIAN
mkdir -p $BLD_DIR/$DATA_DIR/gac
mkdir -p $REPO_DIR/build/deb

cp $REPO_DIR/build/src/* $BLD_DIR/$DATA_DIR/gac/
cp $REPO_DIR/LICENSE $BLD_DIR/$DATA_DIR/gac/
cp $REPO_DIR/VERSION $BLD_DIR/$DATA_DIR/gac/

cat << EOF > $BLD_DIR/$DATA_DIR/gac/gac
#!/bin/bash
/usr/bin/env python3 $DATA_DIR/gac/gaccli.pyc "\$@"
EOF

chmod +x $BLD_DIR/$DATA_DIR/gac/gac

cat << EOF > $BLD_DIR/$DATA_DIR/gac/gac_daemon.service
[Unit]
Description=git-auto-commiter (GAC) daemon
After=network.target

[Service]
ExecStart=/usr/bin/env python3 $DATA_DIR/gac/gacmain.pyc
Restart=always
User=$USER
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

cat << EOF > $BLD_DIR/DEBIAN/control
Package: $NAME
Version: $VERSION
Architecture: all
Maintainer: Matthew Nesbitt
Description: A simple CLI tool for automating frequent git commits.
Depends: python3 (>= 3.5), python3-gevent, bash
EOF

cat << EOF > $BLD_DIR/DEBIAN/postinst
#!/bin/bash
ln -s $BLD_DIR/$DATA_DIR/gac/gac $BIN_DIR/gac
ln -s $BLD_DIR/$DATA_DIR/gac/gac_daemon.service $UNIT_DIR/gac_daemon.service
sudo systemctl daemon-reload
EOF

cat << EOF > $BLD_DIR/DEBIAN/postrm
#!/bin/bash
rm $BIN_DIR/gac
rm $UNIT_DIR/gac_daemon.service
sudo systemctl daemon-reload
EOF

chmod +x $BLD_DIR/DEBIAN/postinst
chmod +x $BLD_DIR/DEBIAN/postrm

rm -rf $REPO_DIR/build/deb/$NAME-$VERSION-1_all.deb
dpkg-deb --build --root-owner-group $BLD_DIR $REPO_DIR/build/deb/
rm -rf $BLD_DIR
