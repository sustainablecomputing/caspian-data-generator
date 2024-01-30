#!/bin/bash

############################################################
#
# Cleanup
#
# Usage: <shellName> [<numClusters>]
#
#         where <numClusters> is the number of clusters
#         (default 1)
#
# Steps:
#  (1) delete clusters
#
############################################################

. demo-setenv.sh

echo "  "
echo "==> CLEANING UP"
echo "  "

numClusters=1
if [[ $1 && $1 -gt 0 ]]
then
	numClusters=$1
fi

echo "==> Deleting ${numClusters} cluster(s)"

set -x


for i in $(seq ${numClusters})
do
	csi="${CLUSTER}${i}"
	k3d cluster delete ${csi}
done

rm -R ${TEMP_DIR}/


set +x
break_continue_message="Stop mcad. Is MCAD terminated?"; continue_prompt

echo ""
echo "==> CLUSTERS DELETED!"
echo ""