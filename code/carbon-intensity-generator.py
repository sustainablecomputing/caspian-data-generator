
import sys
import time

import subprocess
kube_path='~/.kube/config'
period_length=60
T=48
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------

def update_carbon():      
        for t in range(T):
             
       
                subprocess.run('cp -f ~/caspian-demo/data/CI/'+str(1+(t%24))+'/CA-ON.csv ~/caspian/monitoring/data/CA-ON.csv ',shell=True)
                subprocess.run('cp -f ~/caspian-demo/data/CI/'+str(1+(t%24))+'/JP-KN.csv ~/caspian/monitoring/data/JP-KN.csv ',shell=True)
                subprocess.run('cp -f ~/caspian-demo/data/CI/'+str(1+(t%24))+'/DE.csv ~/caspian/monitoring/data/DE.csv ',shell=True)
                time.sleep(period_length)
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------

 
if len(sys.argv)>1:
     
    period_length=int(sys.argv[1])
update_carbon()