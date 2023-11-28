#!/bin/bash
# Change to the directory containing the Python script
cd ~/mcad
go run ./cmd/main.go --kube-context=kind-hub --mode=dispatcher --metrics-bind-address=127.0.0.1:8084 --health-probe-bind-address=127.0.0.1:8085 &

go run ./cmd/main.go --kube-context=kind-spoke1 --mode=runner --metrics-bind-address=127.0.0.1:8082 --health-probe-bind-address=127.0.0.1:8083 --clusterinfo-name=spoke1 --geolocation=CA-ON &
node ~/mcad/syncer/syncer.js kind-hub kind-spoke1 default spoke1 &

#go run ./cmd/main.go --kube-context=kind-spoke3 --mode=runner --metrics-bind-address=127.0.0.1:8086 --health-probe-bind-address=127.0.0.1:8087 --clusterinfo-name=spoke1 --geolocation=CA-ON &
#node ~/mcad/syncer/syncer.js kind-hub kind-spoke3 default spoke3



go run ./cmd/main.go --kube-context=kind-spoke4 --mode=runner --metrics-bind-address=127.0.0.1:8088 --health-probe-bind-address=127.0.0.1:8089 --clusterinfo-name=spoke4 --geolocation=US-TEX-ERCO &
node ~/mcad/syncer/syncer.js kind-hub kind-spoke4 default spoke4

