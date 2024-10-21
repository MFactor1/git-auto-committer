#!/bin/sh
if [ ! -d "./build" ]; then
	echo "Creating build dir"
fi

./compile
