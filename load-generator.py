import datetime
import math 
import os
import sys
import time
import numpy 
from scipy.stats import poisson
import random
import kubernetes
from kubernetes import client,utils
from kubernetes.config import kube_config
from kubernetes.client.rest import ApiException
import subprocess
kube_path='~/.kube/config'

n=1             # number of jobs
TT = 1          # number of time slots to gegerate load
period_length=60
Overal_T=48
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
# for a given job id,  if there is no job in workspace with that name, it creates greenjob object, namespace, and a deployment inside that namespace 
def create_job(job_id,run_time,duration,deadline,cpu,gpu):   
        
       
        path=os.path.expanduser('~')+"/caspian-demo"
        os.chdir(path+"/script")
        os.system('./create-aw.sh aw'+str(job_id)+"\t"+str(run_time)+"\t"+str(duration)+"\t"+str(deadline)+"\t"+str(cpu)+"\t"+str(gpu))
        subprocess.run('kubectl config use-context k3d-hub ',shell=True)
    
        subprocess.run(' kubectl apply -f'+path+'/temp/aw'+str(job_id)+'.yaml',shell=True)
        
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
#create jobs for a time horizon T
def create_all_jobs():
    numpy.random.seed(1)
    subprocess.run('kubectl config use-context k3d-hub ',shell=True)
               
    if len(sys.argv)>2:
        T=int(sys.argv[1])
        n=int(sys.argv[2])
        path=os.path.expanduser('~')+"/caspian-demo/script"
        os.chdir(path)
        rate = n / T
       # ps=poisson.rvs(rate, size=T)
        ps=numpy.random.poisson(rate, size=T)
        print(ps)
        
        
       
        job_id=0
        for t in range(T):
            for i in range(ps[t]):
                
               
                now=datetime.datetime.utcnow()
                print(now)
              #  datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                l=period_length*(1+numpy.random.randint(0,5))
                d = (now+ datetime.timedelta(0,2*l)).strftime('%Y-%m-%dT%H:%M:%SZ')
                print(d)
                cpu=0#float(1+numpy.random.randint(0,2))/15
                gpu=int(3+numpy.random.randint(0,8))
                create_job(job_id,l,l,d,cpu,gpu)
                job_id=job_id+1
            subprocess.run('KUBECONFIG='+kube_path+' kubectl get appwrappers',shell=True)
            if t==1:
                subprocess.run('kubectl config use-context k3d-cluster1 ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster1-server-0 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent -- > ~/caspian-demo/util/util-spoke1.txt ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster1-agent-0 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent  -- >  ~/caspian-demo/util/util-spoke1-w1.txt ',shell=True)
               # subprocess.run('kubectl describe node k3d-cluster1-agent-1 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent  -- >  ~/caspian-demo/util/util-spoke1-w2.txt ',shell=True)
                subprocess.run('kubectl config use-context k3d-cluster2 ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster2-server-0 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent  -- >  ~/caspian-demo/util/util-spoke2.txt ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster2-agent-0 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent  -- >  ~/caspian-demo/util/util-spoke2-w1.txt ',shell=True)
                #subprocess.run('kubectl describe node k3d-cluster2-agent-1 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent  -- >  ~/caspian-demo/util/util-spoke2-w2.txt ',shell=True)
                subprocess.run('kubectl config use-context k3d-cluster3 ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster3-server-0 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent  -- >  ~/caspian-demo/util/util-spoke3.txt ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster3-agent-0 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent  -- >  ~/caspian-demo/util/util-spoke3-w1.txt ',shell=True)
               
            if t>1:
                    
                    subprocess.run('kubectl config use-context k3d-cluster1 ',shell=True)
                    subprocess.run('kubectl describe node k3d-cluster1-server-0 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent  -- >>  ~/caspian-demo/util/util-spoke1.txt ',shell=True)
                    subprocess.run('kubectl describe node k3d-cluster1-agent-0 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent  -- >>  ~/caspian-demo/util/util-spoke1-w1.txt ',shell=True)
                   # subprocess.run('kubectl describe node k3d-cluster1-agent-1 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent  -- >>  ~/caspian-demo/util/util-spoke1-w2.txt ',shell=True)
                    subprocess.run('kubectl config use-context k3d-cluster2 ',shell=True)
                    subprocess.run('kubectl describe node k3d-cluster2-server-0 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent  -- >>  ~/caspian-demo/util/util-spoke2.txt ',shell=True)
                    subprocess.run('kubectl describe node k3d-cluster2-agent-0 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent  -- >>  ~/caspian-demo/util/util-spoke2-w1.txt ',shell=True)
                    #subprocess.run('kubectl describe node k3d-cluster2-agent-1 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent  -- >>  ~/caspian-demo/util/util-spoke2-w2.txt ',shell=True)
                    subprocess.run('kubectl config use-context k3d-cluster3 ',shell=True)
                    subprocess.run('kubectl describe node k3d-cluster3-server-0 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent  -- >>  ~/caspian-demo/util/util-spoke3.txt ',shell=True)
                    subprocess.run('kubectl describe node k3d-cluster3-agent-0 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent  -- >>  ~/caspian-demo/util/util-spoke3-w1.txt ',shell=True)
                   
                    subprocess.run('cp -f ~/caspian-demo/CI/'+str(t-1)+'/CA-ON.csv ~/caspian/monitoring/data/CA-ON.csv ',shell=True)
                    subprocess.run('cp -f ~/caspian-demo/CI/'+str(t-1)+'/JP-KN.csv ~/caspian/monitoring/data/JP-KN.csv ',shell=True)
                    subprocess.run('cp -f ~/caspian-demo/CI/'+str(t-1)+'/DE.csv ~/caspian/monitoring/data/DE.csv ',shell=True)
            time.sleep(period_length)
        

        for t in range(T,Overal_T):  
                subprocess.run('kubectl config use-context k3d-cluster1 ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster1-server-0 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent  -- >>  ~/caspian-demo/util/util-spoke1.txt ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster1-agent-0 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent  -- >>  ~/caspian-demo/util/util-spoke1-w1.txt ',shell=True)
               # subprocess.run('kubectl describe node k3d-cluster1-agent-1 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent  -- >>  ~/caspian-demo/util/util-spoke1-w2.txt ',shell=True)
                subprocess.run('kubectl config use-context k3d-cluster2 ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster2-server-0 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent  -- >>  ~/caspian-demo/util/util-spoke2.txt ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster2-agent-0 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent -- >>  ~/caspian-demo/util/util-spoke2-w1.txt ',shell=True)
               # subprocess.run('kubectl describe node k3d-cluster2-agent-1 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent  -- >>  ~/caspian-demo/util/util-spoke2-w2.txt ',shell=True)
                subprocess.run('kubectl config use-context k3d-cluster3 ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster3-server-0 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent  -- >>  ~/caspian-demo/util/util-spoke3.txt ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster3-agent-0 | grep Allocated -A 15 | grep -ve Event -ve Allocated -ve percent -- >>  ~/caspian-demo/util/util-spoke3-w1.txt ',shell=True)
                   
                subprocess.run('cp -f ~/caspian-demo/CI/'+str((t-1)%24)+'/CA-ON.csv ~/caspian/monitoring/data/CA-ON.csv ',shell=True)
                subprocess.run('cp -f ~/caspian-demo/CI/'+str((t-1)%24)+'/JP-KN.csv ~/caspian/monitoring/data/JP-KN.csv ',shell=True)
                subprocess.run('cp -f ~/caspian-demo/CI/'+str((t-1)%24)+'/DE.csv ~/caspian/monitoring/data/DE.csv ',shell=True)
                time.sleep(period_length)
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------

 

create_all_jobs()