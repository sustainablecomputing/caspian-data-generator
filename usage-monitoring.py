import subprocess
import time


T=48
period_length=60
subprocess.run('cd ~/caspian-demo ',shell=True)
for t in range(T):
            if t==0:
              
                subprocess.run('kubectl config use-context kind-spoke1 ',shell=True)
                subprocess.run('kubectl describe node spoke1-control-plane | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- > util-spoke1.txt ',shell=True)
                subprocess.run('kubectl config use-context kind-spoke4 ',shell=True)
                subprocess.run('kubectl describe node spoke4-control-plane | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- > util-spoke4.txt ',shell=True)
                subprocess.run('kubectl describe node spoke4-worker | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- > util-spoke4-w1.txt ',shell=True)
                subprocess.run('kubectl describe node spoke4-worker2 | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- > util-spoke4-w2.txt ',shell=True)
            if t>0:
                subprocess.run('kubectl config use-context kind-spoke1 ',shell=True)
                subprocess.run('kubectl describe node spoke1-control-plane | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- >> util-spoke1.txt ',shell=True)
                subprocess.run('kubectl config use-context kind-spoke4 ',shell=True)
                subprocess.run('kubectl describe node spoke4-control-plane | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- >> util-spoke4.txt ',shell=True)
                subprocess.run('kubectl describe node spoke4-worker | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- >> util-spoke4-w1.txt ',shell=True)
                subprocess.run('kubectl describe node spoke4-worker2 | grep Allocated -A 10 | grep -ve Event -ve Allocated -ve percent -ve -- >> util-spoke4-w2.txt ',shell=True)
           
            time.sleep(period_length)
        
        
  
