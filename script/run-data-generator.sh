#!/bin/bash

############################################################
#
# Create AppWrappers in a timely manner (poisson) and submit them to the hub cluster
#
# Usage: <shellName> [<numSlots>] [<numJobs>] 
# Arguments
# $1  number of time slots to simulate workload arrivals
# $2  Number of jobs be submitted over numSlots slots
############################################################
if [ $# -lt 2 ]
then
	echo "usage: <cmd> <numSlots> <numJobs> "
	exit
fi


. setenv.sh
mkdir -p $TEMP_DIR
numClusters=1
if [[ $1 && $1 -gt 0 ]]
then
	numSlots=$1
fi

numJobs=1
if [[ $2 && $2 -gt 0 ]]
then
	numJobs=$2
fi



hub_context=${CONTEXT_PREFIX}${HUB}
cd ~/caspian-demo

/usr/bin/python3 ~/caspian-demo/code/load-generator.py $numSlots $numJobs $hub_context $PERIOD_LENGTH &

/usr/bin/python3 ~/caspian-demo/code/carbon-intensity-generator.py  $PERIOD_LENGTH&
