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
export PERIOD_LENGTH=30
export OPTIMIZATION_MODE="sustainable"