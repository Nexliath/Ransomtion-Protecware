#!/bin/bash

pyinstaller -F daemon/main.py -n "RansomtionProtecware-daemon" -y
if [ `uname -s` = "Darwin" ]; then
	echo "base64 = \"$(base64 -b 0 ./dist/RansomtionProtecware-daemon)\"" > gui/daemon.py
else
	echo "base64 = \"$(base64 -w 0 ./dist/RansomtionProtecware-daemon)\"" > gui/daemon.py
fi

rm -rf build/*

pyinstaller -F gui/main.py -n "RansomtionProtecware" -i gui/assets/logo.ico -y

rm -rf build/*
