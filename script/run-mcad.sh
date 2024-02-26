#!/bin/bash
############################################################
#
# run-mcad
#
# Usage: <shellName> [<numClusters>]
#
#         where <numClusters> is the number of spoke clusters
#         (default 1)
#
# Steps:
#  (1) Install MCAD in hub 
#  (2) Run MCAD Dispatcher in hub
#  For each spoke cluster i in {1,2,...,numClusters}
#  (3) Install MCAD 
#  (4) Run MCAD Runner in spoke
#  (5) Run syncer for syning between hub and the spoke
############################################################


numClusters=1
if [[ $1 && $1 -gt 0 ]]
then
	numClusters=$1
fi

. setenv.sh

#Step(1): 
cd $MCAD_DIR
hub_context=${CONTEXT_PREFIX}${HUB}
kubectl config use-context $hub_context
make install

#Step (2):
go run ./cmd/main.go --kube-context=$hub_context --mode=dispatcher --metrics-bind-address=127.0.0.1:8080 --health-probe-bind-address=127.0.0.1:8081 &

#MCAD Runner gets as input the geo-location and power profile of the clusters and update 
# the clusterinfo accordingly. A sample input values for 10 clusters are provided below.

#Step (3)-(5)
for i in $(seq ${numClusters});
do
    csi="${CLUSTER}${i}"
    spoke_context=${CONTEXT_PREFIX}${csi}
    kubectl config use-context ${spoke_context}
    make install
    go run ./cmd/main.go --kube-context=${spoke_context} --mode=runner --metrics-bind-address=127.0.0.1:${metrics_ports[i]} --health-probe-bind-address=127.0.0.1:${health_ports[i]} --clusterinfo-name=${csi} --geolocation=${zones[i]} --power-idle=${idealPower[i]} --power-peak=${peakPower[i]}&
    node ./syncer/syncer.js $hub_context   $spoke_context default $csi   &

done 

