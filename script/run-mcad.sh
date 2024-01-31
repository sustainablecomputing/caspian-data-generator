#!/bin/bash


numClusters=1
if [[ $1 && $1 -gt 0 ]]
then
	numClusters=$1
fi

. demo-setenv.sh


zones=("CA-ON" "DE" "JP-KN" "GB" "AU-TAS" "FR" "US-TEX-ERCO" "US-NY-NYIS" "US-CAL-CISO" "IN-EA") #geo-location of clusters
idealPower=(100 100 100 100 100 100 100 100 100 100)  #average ideal power of each cluster
peakPower=(300 300 300 330 300 300 300 300 300 300)    #average peak power of each cluster
ports1=(8081 8082 8083 8084 8085 8086 8087 8088 8089 8090)  #ports used in metrics-bind-address
ports2=(8091 8092 8093 8094 8095 8096 8097 8098 8099 8100)  #ports used in health-probe-bind-address


cd $MCAD_DIR
hub_context=${CONTEXT_PREFIX}${HUB}
kubectl config use-context $hub_context
make install
go run ./cmd/main.go --kube-context=$hub_context --mode=dispatcher --metrics-bind-address=127.0.0.1:8080 --health-probe-bind-address=127.0.0.1:8081 &
set -x

for i in $(seq ${numClusters});
do
    csi="${CLUSTER}${i}"
    spoke_context=${CONTEXT_PREFIX}${csi}
    kubectl config use-context ${spoke_context}
    make install
    go run ./cmd/main.go --kube-context=${spoke_context} --mode=runner --metrics-bind-address=127.0.0.1:${ports1[i]} --health-probe-bind-address=127.0.0.1:${ports2[i]} --clusterinfo-name=${csi} --geolocation=${zones[i]} &
    node ./syncer/syncer.js "${hub_context}"   "${spoke_context}" default "${csi}"   &

done 

set +x