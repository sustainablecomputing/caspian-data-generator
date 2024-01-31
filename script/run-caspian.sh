#!/bin/bash
. demo-setenv.sh
cd $CASPIAN_DIR
context=${CONTEXT_PREFIX}${HUB}
go run ./cmd/main.go --kube-context=$context --optimizer=sustainable #optimizer could work in two-modes: sustainable or QoS
