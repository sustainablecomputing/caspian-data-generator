#!/bin/bash
# Change to the directory containing the Python script
cd ~/caspian
go run ./cmd/main.go --kube-context=k3d-hub --optimizer=sustainable //optimizer good be sustaible or QoS
