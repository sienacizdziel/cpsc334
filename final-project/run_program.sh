#!/bin/bash

while ! ping -c1 github.com
do
	echo "waiting for github..."
	sleep 1
done

cd ~/Desktop/cpsc334/final_project
export DISPLAY=":0"
python3 final_project.py > out.txt
cd ~
