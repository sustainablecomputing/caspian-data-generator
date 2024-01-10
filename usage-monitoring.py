import subprocess
import time


T=48
period_length=60
subprocess.run('cd ~/caspian-demo ',shell=True)
for t in range(T):
            if t==0:
              
                subprocess.run('kubectl config use-context k3d-cluster1 ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster1-server-0 | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- > util-spoke1.txt ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster1-agent-0 | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- > util-spoke1-w1.txt ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster1-agent-1 | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- > util-spoke1-w2.txt ',shell=True)
                subprocess.run('kubectl config use-context k3d-cluster2 ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster2-server-0 | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- > util-spoke2.txt ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster2-agent-0 | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- > util-spoke2-w1.txt ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster2-agent-1 | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- > util-spoke2-w2.txt ',shell=True)
                subprocess.run('kubectl config use-context k3d-cluster3 ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster3-server-0 | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- > util-spoke3.txt ',shell=True)
                

            if t>0:
                subprocess.run('kubectl config use-context k3d-cluster1 ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster1-server-0 | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- >> util-spoke1.txt ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster1-agent-0 | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- >> util-spoke1-w1.txt ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster1-agent-1 | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- >> util-spoke1-w2.txt ',shell=True)
                subprocess.run('kubectl config use-context k3d-cluster2 ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster2-server-0 | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- >> util-spoke2.txt ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster2-agent-0 | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- >> util-spoke2-w1.txt ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster2-agent-1 | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- >> util-spoke2-w2.txt ',shell=True)
                subprocess.run('kubectl config use-context k3d-cluster3 ',shell=True)
                subprocess.run('kubectl describe node k3d-cluster3-server-0 | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- >> util-spoke3.txt ',shell=True)
                
            time.sleep(period_length)
        
        
  
