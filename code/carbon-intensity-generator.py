
import sys
import time

import subprocess
kube_path='~/.kube/config'
period_length=120
T=60
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------

def update_carbon():      
        for t in range(T):
             
       
                subprocess.run('cp -f ~/caspian-demo/data/CI/'+str(t)+'/CA-ON.csv ~/caspian/monitoring/data/CA-ON.csv ',shell=True)
                subprocess.run('cp -f ~/caspian-demo/data/CI/'+str(t)+'/JP-KN.csv ~/caspian/monitoring/data/JP-KN.csv ',shell=True)
                subprocess.run('cp -f ~/caspian-demo/data/CI/'+str(t)+'/DE.csv ~/caspian/monitoring/data/DE.csv ',shell=True)
                time.sleep(period_length)
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------

 
if len(sys.argv)>1:
     
    period_length=int(sys.argv[1])
update_carbon()