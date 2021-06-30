#!/bin/bash

pyinstaller -F daemon/main.py -n "RansomtionProtecware-daemon" -y
pyinstaller -F gui/main.py -n "RansomtionProtecware" -i gui/assets/logo.ico -y

mkdir -p /var/lib/ransomtion-protecware
cp ./dist/RansomtionProtecware-daemon /var/lib/ransomtion-protecware/daemon
