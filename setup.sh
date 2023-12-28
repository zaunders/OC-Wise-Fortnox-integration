#!/bin/bash

# Update package list
sudo apt-get update

# Install Python 3
sudo apt-get install python3 -y

# Install pip
sudo apt-get install python3-pip -y

# Install Python packages
pip3 install numpy python-dotenv requests datetime reportlab -y
apt install python3-numpy

# reset numpy files
python3 reset_numpy_tracking_lists.py

# Make directories for pdfs and json files
mkdir json_files
mkdir pdfs

# Things to do:
# - change paths to .env file
# - reset numpy files
# 
