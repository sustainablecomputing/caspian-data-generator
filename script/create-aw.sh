#!/bin/bash

# create an appwrapper  yaml file in a temp directory from a template file
#  - substitute original strings ending with "-xxx" in the template file
#    with values given in the arguments
#  - name of generated yaml file is the given job name
#
# Arguments
# $1  unique job name
# $2  cpu execution time in seconds
# $3	total run time in seconds
# $4	deadline in real time
# $5	number of cpu cores
# $6	number of gpu cores

if [ $# -lt 6 ]
then
	echo "usage: <cmd> <job-name> <run-time> <duration> <deadline> <cpu-cores> <gpu-cores>"
	exit
fi


job_name=$1
run_time=$2
duration=$3
deadline=$4
cpu_core=$5
gpu_core=$6

. setenv.sh

echo "==> creating AppWrapper file ${job_name}.yaml"



sed 's/job-xxx/'"$job_name"'/' ${YAML_DIR}/aw-template.yaml | \
sed 's/rrr/'"$run_time"'/' | \
sed 's/ttt/'"$duration"'/' | \
sed 's/ddd/'"$deadline"'/' | \
sed 's/ggg/'"$gpu_core"'/' | \
sed 's/ccc/'"$cpu_core"'/' > \
${TEMP_DIR}/${job_name}.yaml
