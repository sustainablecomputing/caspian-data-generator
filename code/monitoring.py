import math
import sys
import kubernetes
from kubernetes.config import kube_config
import collections
from kubernetes.client.rest import ApiException
collections.Callable = collections.abc.Callable
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd   

# Monitoring: - retrieve the specs of clusterinfo objects in the hub and plot the info
class Monitoring(object):
    contxt="k3d-hub"
    kube_config="~/.kube/config"   
    
    api_client=None
    api_instance=None

    frequency=60                # frequency of updating the plot (every 60 seconds)
    
    clusterInfos=[]             # clusterInfo objects in the hub
    T=72                    # number of time slots. Each slot is 6*60 seconds
    perSlot=6                      #number of bars  per slot to display  
    M=3                         # number of available clusterinfo (default value is 3)
 
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
# create client to talk to the hub
    def __init__(self,hub_context,frequency):         
        self.api_client=kube_config.new_client_from_config(config_file=self.kube_config,context=self.contxt)
        self.api_instance = kubernetes.client.CustomObjectsApi(self.api_client)
        self.contxt=hub_context
        self.frequency=frequency
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
# get clusterInfo objects living in the hub and update the list of clusterInfos
    def get_clusterInfos(self):
        group = 'workload.codeflare.dev' 
        version = 'v1beta1' 
        plural = 'clusterinfo' 
        self.clusterInfos=[]
        
        print("\nCluster Infos:\n")
      
        try:
            api_response = self.api_instance.list_cluster_custom_object( group, version, plural,timeout_seconds=2,   watch=False)
            clusterinfos=api_response.get('items')           
            
            for ci in clusterinfos:
               
                if 'usage' in ci['status'] and 'nvidia.com/gpu' in ci['status']['usage']:
                    tmp = { 'name':ci['metadata']['name'],'gpu':ci['status']['usage']['nvidia.com/gpu'],'gpu-cap':ci['status']['capacity']['nvidia.com/gpu'],'carbon': ci['spec']['carbon']}
                else:
                   tmp = { 'name':ci['metadata']['name'],'gpu':'0','gpu-cap':ci['status']['capacity']['nvidia.com/gpu'],'carbon': ci['spec']['carbon']}
                
                self.clusterInfos.append(tmp)    
                print(tmp['gpu'])                     
        except ApiException as e:
            print("Exception when calling CustomObjectsApi->get_cluster_custom_object: %s\n" % e)

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
    def compute_slowdown(self):
        group = 'workload.codeflare.dev' 
        version = 'v1beta1' 
        plural = 'appwrappers' 
        aws=[]
        avg_slowdown=0
        
       
      
        try:
            api_response = self.api_instance.list_cluster_custom_object( group, version, plural,timeout_seconds=2,   watch=False)
            aws=api_response.get('items')           
            
            for aw in aws:
                remainTime=0
                TimeDispatched=0
                print(aw['metadata']['name']) 
                if  aw['spec']['dispatcherStatus']['phase']== "Succeeded":
                  responseTime=1.0#aw['spec']['dispatcherStatus']['transitions'][lenn-1]-aw['creationTimestamp']
                  avg_slowdown+=(responseTime/aw['spec']['sustainable']['runTime'])
                else:
                    if aw['spec']['dispatcherStatus']['phase']== "Queued" or aw['spec']['dispatcherStatus']['phase']== "Dispatching" or aw['spec']['dispatcherStatus']['phase']== "Running"or aw['spec']['dispatcherStatus']['phase']== "Requeuing":
                        TimeDispatched = aw['spec']['dispatcherStatus']['timeDispatched']
                    if aw['spec']['dispatcherStatus']['phase'] != "Queued" :
                        TimeDispatched += 10#int64(time.Since(aw.Spec.DispatcherStatus.LastDispatchingTime.Time).Seconds())
                    remainTime = 10#(aw['spec']['sustainable']['runTime']-TimeDispatched) / PeriodLength
                    if aw['spec']['sustainable']['runTime'] == 0: 
                        remainTime = 2#int64(math.Ceil(float64(core.DefaultRunTime-int(TimeDispatched)) / float64(s.PeriodLength)))

			                            
        except ApiException as e:
            print("Exception when calling CustomObjectsApi->get_cluster_custom_object: %s\n" % e)

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
hub_context="k3d-hub"
frequency=60
if len(sys.argv)>2:
     hub_context=str(sys.argv[0])
     frequency=int(sys.argv[1])
m=Monitoring(hub_context,frequency)
T=m.T
M=m.M


utilization= [[0 for i in range(T)] for j in range(M)]
em_rate=[0]*T
#slow_down: for test
slow_down=[1,1,1,1.2,1.2,1.4,1.4,1.3,1.4,1.5,1.4,1.5,1.6,1.5,1.5,1.6,1.6,1.7,1.7,1.5,1.7,1.6,1.7,1.6,1.5,1.6,1.5,1.5,1.6,1.6,1.7,1.7,1.5,1.5,1.6,1.5]
lateness=[1,1,1,1.2,1.2,1,1.1,1.1,1.3,1.3,1.2,1.2,1.3,1.3,1.1,1.1,1.2,1.7,1.2,1.5,1.7,1.1,1.4,1.6,1.5,1.1,1.1,1.3,1.2,1.3,1.2,1.4,1.1,1.5,1.2,1.2]

carbonIntensity=[[0 for i in range(T)] for j in range(M)]

carbon_metric=[0]*T
lateness_ratio=[0]*T
slow_down_ratio=[0]*T
ax=[]
ax2=[]
colors=['green','red', 'brown']
fig = plt.figure("Cluster Performance",figsize=(9,6))
fig2 = plt.figure("Overall Performance",figsize=(9,3))


for j in range(M):
    ax.append(fig.add_subplot(2,M,j+1))

for j in range(M):
 ax.append(fig.add_subplot(2,M,j+M+1))

for j in range(3):
 ax2.append(fig2.add_subplot(1,3,1+j))

def animate_cluster(i):
    m.get_clusterInfos()
    for j in range(M):
        for t in range(0,24):
            if i+t<T:
                carbonIntensity[j][t+i]=int(m.clusterInfos[0]['carbon'][t])#dframe.iloc[int(t/m.perSlot)][zones[j]]
    if i>0:
        carbon_metric[i]=carbon_metric[i-1]
        
   
    for j in range(M):
        utilization[j][i]=float(m.clusterInfos[0]['gpu'])/float(m.clusterInfos[0]['gpu-cap'])#test: (3-j)*0.15#
        
     
    xs=range(0,T)

    for j in range(M):  
        ax[j].clear()
        ax[j].axis([0, T, 0, 700.1])
        ax[j].set_xticks(ticks=range(5,T+1,5),labels=range(5,T+1,5),fontsize=5) #every 6 bars add label of slot
        ax[j].set_yticks(ticks=range(100,700,100),labels=range(100,700,100),fontsize=5)
        ax[j].set_ylabel('Carbon Intensity', fontsize = 8)
        ax[j].set_xlabel('Time slots', fontsize = 8)
        ax[j].step(xs, carbonIntensity[j],color =colors[j])
        ax[j].set_title('Spoke '+ str(j+1), fontsize=10)

        ax[j+M].clear()
        ax[j+M].axis([0, T, 0, 1.1])
        ax[j+M].set_yticks(ticks=range(0,2),labels=range(0,2,1),fontsize=5)
        ax[j+M].set_xticks(ticks=range(5,T+1,5),labels=range(5,T+1,5),fontsize=5) #every 6 bars add label of slot
        ax[j+M].set_ylabel('GPU utilization', fontsize = 8)
        ax[j+M].set_xlabel('Time slots', fontsize = 8)
        ax[j+M].bar(xs, utilization[j],color =colors[j])
        

ani1 = animation.FuncAnimation(fig, animate_cluster,interval=m.frequency*1000)       



def animate2(i):
    slow_down_ratio[i]=slow_down[i]
    lateness_ratio[i]=lateness[i] 
    if i>0:
        carbon_metric[i]=carbon_metric[i-1]
        
    for j in range(M):
        carbon_metric[i]=carbon_metric[i]+(utilization[j][i] *carbonIntensity[j][i])
        
    
    xs=range(0,T)

    for j in range(3):   

        ax2[j].clear()
        ax2[j].set_xticks(ticks=range(5,T+1,5),labels=range(5,T+1,5),fontsize=5) #every 6 bars add label of slot
        ax2[j].set_xlabel('Time slots', fontsize = 8)
        if j==0:
            ax2[j].axis([0, T, 0, 10000.1])
            ax2[j].bar(xs, carbon_metric,color ='blue')
            ax2[j].set_yticks(ticks=range(1000,10000,1000),labels=range(1000,10000,1000),fontsize=5)
            ax2[j].set_ylabel('Carbon Emission', fontsize = 8)
        if j==1:
            ax2[j].axis([0, T, 0, 3.1])
            ax2[j].bar(xs, slow_down_ratio,color ='blue')
            ax2[j].set_yticks(ticks=range(0,3,1),labels=range(0,3,1),fontsize=5)
            ax2[j].set_ylabel('Slow down', fontsize = 8)
        
        if j==2:
            ax2[j].axis([0, T, 0, 3.1])
            ax2[j].bar(xs, lateness_ratio,color ='blue')
            ax2[j].set_yticks(ticks=range(0,3,1),labels=range(0,3,1),fontsize=5)
            ax2[j].set_ylabel('Lateness ratio', fontsize = 8)
  
ani2 = animation.FuncAnimation(fig2, animate2,interval=m.frequency*1000)

plt.show()
    