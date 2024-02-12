#!/bin/bash

############################################################
#
# watch sttatus of appwrappers ad clusterinfos and plot 
############################################################



hub_context=${CONTEXT_PREFIX}${HUB}
cd ~/caspian-demo

/usr/bin/python3 ~/caspian-demo/code/monitoring.py  $hub_context $PERIOD_LENGTH
