#!/bin/bash

############################################################
#
# Create a multi-cluster environment with one hub cluster and multi spoke clusters (all k3d clusters)
#
# Usage: <shellName> [<numClusters>] [<numNodes>] [<numGPUs>]
# Arguments
# $1  number of spoke clusters
# $2  Number of nodes in each spoke
# $3	Number of GPU cores in each node

# Steps:
# (1) Create a hub cluster 
#  For each spoke cluster i in {1,2,...,numClusters}
#  (2) Create the cluster (clusteri) with numNodes nodes
#  (3) Add numGPUs GPUs in each node

#
############################################################

if [ $# -lt 3 ]
then
	echo "usage: <cmd> <num-spokes> <num-nodes> <num-gpus> "
	exit
fi


. demo-setenv.sh

numClusters=1
if [[ $1 && $1 -gt 0 ]]
then
	numClusters=$1
fi

numNodes=2
if [[ $2 && $2 -gt 0 ]]
then
	numNodes=$2
fi


numGPUs=16
if [[ $3 && $3 -gt 0 ]]
then
	numGPUs=$3
fi

#
echo ""
echo "==> Creating and setting $numClusters k3d cluster(s)"
set -x
k3d cluster create hub
for i in $(seq ${numClusters})
do
	csi="${CLUSTER}${i}"

	# create k3d cluster 
	
	k3d cluster create ${csi} --agents $numNodes
	# now context is ${csi}
	. extend_resources.sh $numGPUs
	
done

set +x

echo ""
echo "==> CLUSTERS READY!"
echo ""