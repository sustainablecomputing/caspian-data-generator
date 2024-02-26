#!/bin/bash


# Functions
function extend-resources {
    # Patch nodes to provide GPUs resources without physical GPUs.
    # This is intended to allow testing of GPU specific features such as histograms.

    # Start communication with cluster
    kubectl proxy --port=0 > .port.dat 2>&1 &
    proxy_pid=$!

    echo "Starting background proxy connection (pid=${proxy_pid})..."
    echo "Waiting for proxy process to start."
    sleep 2

    kube_proxy_port=$(cat .port.dat | awk '{split($5, substrings, ":"); print substrings[2]}')
    curl -s 127.0.0.1:${kube_proxy_port} > /dev/null 2>&1

    if [[ ! $? -eq 0 ]]; then
        echo "Calling 'kubectl proxy' did not create a successful connection to the kubelet needed to patch the nodes. Exiting."
        kill -9 ${proxy_pid}
        exit 1
    else
        echo "Connected to the kubelet for patching the nodes. Using port ${kube_proxy_port}."
    fi

    rm .port.dat

    # Variables
  
    # Patch nodes
    action="$1"
    resource_name="nvidia.com~1gpu"
    resource_count="$2" #"16"

    if [[ ${action} == "add" ]]; then
        for node_name in $(kubectl get nodes --no-headers -o custom-columns=":metadata.name")
        do
            echo "- Patching node (add): ${node_name}"

            patching_status=$(curl -s --header "Content-Type: application/json-patch+json" \
                                      --request PATCH \
                                      --data '[{"op": "add", "path": "/status/capacity/'${resource_name}'", "value": "'${resource_count}'"}]' \
                                      http://localhost:${kube_proxy_port}/api/v1/nodes/${node_name}/status | jq -r '.status')

            if [[ ${patching_status} == "Failure" ]]; then
                echo "Failed to patch node '${node_name}' with GPU resources"
                exit 1
            fi

            echo "Patching done!"
        done

    elif [[ ${action} == "remove" ]]; then
        for node_name in $(kubectl get nodes --no-headers -o custom-columns=":metadata.name")
        do
            echo "- Patching node (remove): ${node_name}"

            patching_status=$(curl -s --header "Content-Type: application/json-patch+json" \
                                      --request PATCH \
                                      --data '[{"op": "remove", "path": "/status/capacity/'${resource_name}'"}]' \
                                      http://localhost:${kube_proxy_port}/api/v1/nodes/${node_name}/status | jq -r '.status')

            if [[ ${patching_status} == "Failure" ]]; then
                echo "Failed to patch node '${node_name}' with GPU resources"
                exit 1
            fi

            echo "Patching done!"
        done

    else
        echo "Nothing to do"

    fi

    # Stop communication with cluster
    echo "Killing proxy (pid=${proxy_pid})..."
    kill -9 ${proxy_pid}
}
numGPUs=16
if [[ $1 && $1 -gt 0 ]]
then
	numGPUs=$1
fi
# Call functions
extend-resources "add" $numGPUs