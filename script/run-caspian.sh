#!/bin/bash
############################################################
#
# run-caspian
#
# Usage: <shellName> [<optimizationMode>]
#
#         where <optimizationMode> could be sustainable or qos
#         (default sustainable)
############################################################
. setenv.sh

if [[ $1 && $1 -gt 0 ]]
then
	optimizationMode=$1
fi

cd $CASPIAN_DIR
context=${CONTEXT_PREFIX}${HUB}
go run ./cmd/main.go --kube-context=$context --optimizer=$OPTIMIZATION_MODE  --period_length=$PERIOD_LENGTH #optimizer could work in two-modes: sustainable or QoS
