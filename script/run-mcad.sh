#!/bin/bash
# Change to the directory containing the Python script
cd ~/mcad

zones=("CA-ON" "DE" "JP-KN" )
idealPower=(100 100 100)
peakPower=(300 300 330)

go run ./cmd/main.go --kube-context=k3d-hub --mode=dispatcher --metrics-bind-address=127.0.0.1:8084 --health-probe-bind-address=127.0.0.1:8085 &

go run ./cmd/main.go --kube-context=k3d-spoke1 --mode=runner --metrics-bind-address=127.0.0.1:8082 --health-probe-bind-address=127.0.0.1:8083 --clusterinfo-name=cluster1 --geolocation=CA-ON &
node ~/mcad/syncer/syncer.js k3d-hub k3d-cluster1 default cluster1 &

go run ./cmd/main.go --kube-context=k3d-spoke2 --mode=runner --metrics-bind-address=127.0.0.1:8080 --health-probe-bind-address=127.0.0.1:8081 --clusterinfo-name=cluster2 --geolocation=DE &
node ~/mcad/syncer/syncer.js k3d-hub k3d-cluster2 default cluster2 &

go run ./cmd/main.go --kube-context=k3d-cspok3 --mode=runner --metrics-bind-address=127.0.0.1:8086 --health-probe-bind-address=127.0.0.1:8087 --clusterinfo-name=cluster3 --geolocation=JP-KN --powerslope=1.15 &
node ~/mcad/syncer/syncer.js k3d-hub k3d-cluster3 default cluster3 