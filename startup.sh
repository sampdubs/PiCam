#!/bin/bash

echo 'this might take a while'
sudo apt-get update
sudo apt-get upgrade
sudo apt-install jq
pip3 install -r requirements.txt
mkdir images
python3 info.py
