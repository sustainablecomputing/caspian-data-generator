# caspian-demo
## Getting Started 
Caspian can be depolyed in Kubernetes cluster. You can use kind or k3d to get  local clusters for testing and running Caspian. For managing containers you can use either Docker Desktop or Rancher Desktop. The instructions below guide you to drop Caspian and its requirements on your local machine and run it for development and testing purposes under k3d cluaters and Rancher Desktop.
### Pre-requisites
- Version 1.19 or higher of [Go](https://go.dev/dl/)

- [kubectl CLI](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/).
- [Git CLI](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
- [Rancher Desktop](https://docs.rancherdesktop.io/getting-started/installation/).
- [k3d](https://k3d.io/v5.6.0/#install-script).

- [clp](https://github.com/lanl/clp). The easiest way to get clp is through [Homebrew](https://brew.sh/).
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

(3) Run MCAD Dispatcher in hub cluster and MCAD Runner in each spoke clusters (m is the number of spoke clusters) by running *./run-mcad* script, 

```
./run-mcad.sh m 
```
For more details on how to setup the charachteristics of cluters (such as their geo-location and power consumption profile) please look at the comments in the script.

(4) Run *run-data-generator* to create workloads (AppWrappers) in a timely manner (poisson) and submit them in the hub cluster,