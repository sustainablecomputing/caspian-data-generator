#!/bin/bash

############################################################
echo "==> setting up environment"
############################################################

############################################################
# Settings
############################################################

# dry run
# set -n

############################################################
# Paths and directories
############################################################

export SCRIPT_DIR=.
export BASE_DIR=..
export YAML_DIR=$BASE_DIR/yaml
export TEMP_DIR=$BASE_DIR/temp
export MCAD_DIR=$HOME/mcad
export CASPIAN_DIR=$HOME/caspian
export CLUSTERS_CONFIG=$HOME/.kube/config

############################################################
# Parameters
############################################################


export CLUSTER=spoke
export HUB=hub
export CONTEXT_PREFIX=k3d-
export PERIOD_LENGTH=120
export OPTIMIZATION_MODE="sustainable" # optimization mode could be qos or sustainable
export zones=("GB" "DE" "JP-KN" "CA-ON" "AU-TAS" "FR" "US-TEX-ERCO" "US-NY-NYIS" "US-CAL-CISO" "IN-EA") #geo-location of clusters
export idealPower=(100 100 100 100 100 100 100 100 100 100)  #average ideal power of each cluster
export peakPower=(300 300 200 300 300 300 300 300 300 300)    #average peak power of each cluster
export metrics_ports=(8081 8082 8083 8084 8085 8086 8087 8088 8089 8090)  #ports used in metrics-bind-address in MCAD
export health_ports=(8091 8092 8093 8094 8095 8096 8097 8098 8099 8100)  #ports used in health-probe-bind-address in MCAD
