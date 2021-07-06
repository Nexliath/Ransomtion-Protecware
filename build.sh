#!/bin/bash

pyinstaller -F daemon/main.py -n "RansomtionProtecware-daemon" -y
echo "base64 = \"$(base64 ./dist/RansomtionProtecware-daemon)\"" > gui/daemon.py

pyinstaller -F gui/main.py -n "RansomtionProtecware" -i gui/assets/logo.ico -y
