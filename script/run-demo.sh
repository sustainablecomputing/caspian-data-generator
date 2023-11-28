#!/bin/bash
# Change to the directory containing the Python script
cd ~/caspian-demo

/usr/local/bin/python3.8 /Users/tbahreini/caspian-demo/load-generator.py 12 80 & #highdemand 12 80, low demand 12 50
/usr/local/bin/python3.8 /Users/tbahreini/caspian-demo/usage-monitoring.py