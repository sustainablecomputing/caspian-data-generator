# Caspian-demo
This repo will enable you to run a dome on using [Caspian](https://github.com/sustainablecomputing/caspian) and [MCAD](https://github.com/project-codeflare/mcad/tree/033081131d23ba30ccf86d7cd7cc63006a51c92d) to schedule and dispatch workloads in a multi-cluster environment to minimize the carbon footprint of execution of workloads. 
## Getting Started 
Caspian can be depolyed in Kubernetes clusters. You can use kind or k3d to get  local clusters for running Caspian. To manage containers, you can use either Docker Desktop or Rancher Desktop. The instructions below guide you to drop Caspian and its requirements on your local machine and run it for development and testing purposes using k3d clusters and Rancher Desktop.

### Pre-requisites
- Version 1.19 or higher of [Go](https://go.dev/dl/)

- [kubectl CLI](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/)
- [Git CLI](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Rancher Desktop](https://docs.rancherdesktop.io/getting-started/installation/)
- [k3d](https://k3d.io/v5.6.0/#install-script)

- [clp](https://github.com/lanl/clp)<br>
The easiest way to get clp is through [Homebrew](https://brew.sh/),
```
brew install clp
``` 
### Clone  repositories
Use Git CLI to clone repositories

-  Clone Caspian repository
```
git clone git@github.com:sustainablecomputing/caspian.git
```

- Clone multicluster branch of MCAD repository
```
git clone git@github.com:tardieu/mcad.git -b multicluster
```

## Steps to deploy Caspian on Mac
(1) Go to the script directory of repo,
```
cd caspian-demo/script
```

(2) Create one hub cluster and multiple spoke clusters by executing the following script, 

```
./create-clusters.sh m n q
```
This script creates one hub cluster and *m* spoke clusters. Here, *n* is the number of worker nodes per cluster and *q* is the number of GPUs per node. For example by calling *./create-clusters.sh 1 1 8*, the script will create one hub cluster and one spoke cluster. There are two nodes on the spoke; one server node, one worker node; each with 8 GPUs.

(3) Run MCAD Dispatcher in hub cluster and MCAD Runner in each spoke clusters by running *./run-mcad* script, 

```
./run-mcad.sh m 
```
Here, *m* is the number of spoke clusters. For more details on how to setup the charachteristics of cluters (such as their geo-location and power consumption profile), please look at the comments in the script.

(4) Run *load-generator.sh* to create workloads (AppWrappers) in a timely manner (poisson distribution) and submit them in the hub cluster,

```
./load-generator.sh T N
```
Here, *T* is the number of time slots in whcih workloads arrive to the system and *N* is the number of workloads to be sumbitted over *T* time slots.

(5) Run Caspian 

```
./run-caspian.sh 
```
The default optimizer in Caspian is a multi-objective optimizer that considers carbon footprint, lateness, and completion time of workloads into consideration when it makes decision. However Caspian provides other options, For example, by passing *qos* parameters to the script, we ask optimizer to only consider lateness and completion time of workloads and do not decide based on the acvailability of low-carbon energy,

```
./run-caspian.sh qos
```