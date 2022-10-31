#!/bin/bash
while ! ping -c1 github.com
do
echo "waiting for github..."
sleep 1
done

cd ~


cd ~/Desktop/cpsc334/raspberrypi
git pull
hostname -I > ip.md
git add ip.md
git commit -m "new ip address!"
git push
cd -
