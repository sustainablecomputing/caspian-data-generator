#!/bin/bash
# Change to the directory containing the Python script
cd ~/caspian-demo

/usr/bin/python3 ~/caspian-demo/load-generator.py 8 80 #& #highdemand 8 80, low demand 8 120
