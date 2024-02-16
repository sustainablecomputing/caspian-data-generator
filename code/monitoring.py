
from dateutil import parser

import sys
import kubernetes
from kubernetes.config import kube_config
import collections
from kubernetes.client.rest import ApiException
collections.Callable = collections.abc.Callable
import matplotlib.pyplot as plt
import matplotlib.animation as animation
  

# Monitoring: - retrieve the specs of clusterinfo objects in the hub and plot the info
class Monitoring(object):
    contxt="k3d-hub"
    kube_config="~/.kube/config"   
    
    api_client=None
    api_instance=None

    frequency=60                # frequency of updating the plot (every 60 seconds)
    
    clusterInfos=[]             # clusterInfo objects in the hub
    T=75                   # number of time slots. Each slot is 6*60 seconds
    slow_down_metric=0                      #number of bars  per slot to display  
    lateness_metric=0
    late_percentage=0
    num_late=0
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
        
        #print("\nCluster Infos:\n")
      
        try:
            api_response = self.api_instance.list_cluster_custom_object( group, version, plural,timeout_seconds=2,   watch=False)
            clusterinfos=api_response.get('items')           
            
            for ci in clusterinfos:
               
                if 'usage' in ci['status'] and 'nvidia.com/gpu' in ci['status']['usage']:
                    tmp = {'geolocation':ci['spec']['geolocation'],'name':ci['metadata']['name'],'gpu':ci['status']['usage']['nvidia.com/gpu'],'gpu-cap':ci['status']['capacity']['nvidia.com/gpu'],'carbon': ci['spec']['carbon']}
                else:
                   tmp = {'geolocation':ci['spec']['geolocation'], 'name':ci['metadata']['name'],'gpu':'0','gpu-cap':ci['status']['capacity']['nvidia.com/gpu'],'carbon': ci['spec']['carbon']}
                
                self.clusterInfos.append(tmp)    
                #print(tmp['gpu'])                     
        except ApiException as e:
            print("Exception when calling CustomObjectsApi->get_cluster_custom_object: %s\n" % e)

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
    def getAppWrappers(self):
        group = 'workload.codeflare.dev' 
        version = 'v1beta1' 
        plural = 'appwrappers' 
        aws=[]
        avg_slowdown=0
        num_succeed=0
        avg_lateness=0
        num_late=0
        #date_format = '%Y-%m-%dT %H:%M:%SZ'
        latenessTime=0
        try:
            api_response = self.api_instance.list_cluster_custom_object( group, version, plural,timeout_seconds=2,   watch=False)
            aws=api_response.get('items')           
            
            for aw in aws:
                
                TimeDispatched=0
               # print(aw['metadata']['name']) 
                if  'dispatcherStatus' in aw['spec'] and (aw['spec']['dispatcherStatus']['phase']== "Succeeded" or (aw['spec']['dispatcherStatus']['phase']== "Queued" and
                'timeDispatched' in aw['spec']['dispatcherStatus'] and  int(aw['spec']['dispatcherStatus']['timeDispatched'])>(130+int(aw['spec']['sustainable']['runTime'])))):
                 
                  lenn = len(aw['spec']['dispatcherStatus']['transitions'])
                  responseTime= (parser.parse (aw['spec']['dispatcherStatus']['transitions'][lenn-1]['time'])- parser.parse (aw['metadata']['creationTimestamp'])).total_seconds()
                  
                  latenessTime= (parser.parse (aw['spec']['dispatcherStatus']['transitions'][lenn-1]['time'])- parser.parse (aw['spec']['sustainable']['deadline'])).total_seconds()-self.frequency*2
                 
                  avg_slowdown+=(responseTime/int(aw['spec']['sustainable']['runTime']))
                  if latenessTime>0:
                    avg_lateness+=(latenessTime/self.frequency)
                    num_late+=1

              

                  num_succeed+=1
            if num_succeed>0:
                m.slow_down_metric=avg_slowdown/(num_succeed)
                m.lateness_metric=100*num_late/num_succeed#avg_lateness/num_succeed
               # print('kk',num_succeed,avg_slowdown/(num_succeed),avg_lateness/num_succeed)
			                            
        except ApiException as e:
            print("Exception when calling CustomObjectsApi->get_cluster_custom_object: %s\n" % e)

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
hub_context="k3d-hub"
frequency=60
if len(sys.argv)>2:
     hub_context=str(sys.argv[1])
     frequency=int(sys.argv[2])
m=Monitoring(hub_context,frequency)
T=m.T
M=m.M


utilization= [[0 for i in range(T)] for j in range(M)]
em_rate=[0]*T
#slow_down: for test
#slow_down=[1,1,1,1.2,1.2,1.4,1.4,1.3,1.4,1.5,1.4,1.5,1.6,1.5,1.5,1.6,1.6,1.7,1.7,1.5,1.7,1.6,1.7,1.6,1.5,1.6,1.5,1.5,1.6,1.6,1.7,1.7,1.5,1.5,1.6,1.5]
#lateness=[1,1,1,1.2,1.2,1,1.1,1.1,1.3,1.3,1.2,1.2,1.3,1.3,1.1,1.1,1.2,1.7,1.2,1.5,1.7,1.1,1.4,1.6,1.5,1.1,1.1,1.3,1.2,1.3,1.2,1.4,1.1,1.5,1.2,1.2]

carbonIntensity=[[0 for i in range(T)] for j in range(M)]

carbon_metric=[0]*T
lateness_ratio=[0]*T
slow_down_ratio=[0]*T
ax=[]
ax2=[]

fig = plt.figure("Cluster Performance",figsize=(9,5.6))
fig2 = plt.figure("Overall Performance",figsize=(9,2.8))


for j in range(M):
    ax.append(fig.add_subplot(2,M,j+1))
    #ax.append( fig.add_axes([0.15+.16*j, 0.6, 0.19+.1*j, 0.25]) )
for j in range(M):
 ax.append(fig.add_subplot(2,M,j+M+1))

for j in range(2):
 ax2.append(fig2.add_subplot(1,2,1+j))
m.get_clusterInfos()
geos=['CA-ON','DE','JP-KN']
geos_full={'CA-ON':'Ontorio, Canada', 'DE':'Germany' ,'JP-KN':'Kansai, Japan'}
colors_geos={'CA-ON':'green','DE':'red', 'JP-KN':'brown'}
positions={}
for j in range(M):
    positions.update({m.clusterInfos[j]['geolocation']:j})

def animate_cluster(i):
    m.get_clusterInfos()
    for jj in range(M):
        j= positions.get(m.clusterInfos[jj]['geolocation'])
        for t in range(0,24):
            if i+t<T:
                carbonIntensity[j][t+i]=int(m.clusterInfos[jj]['carbon'][t])#dframe.iloc[int(t/m.perSlot)][zones[j]]
        utilization[j][i]=100*float(m.clusterInfos[jj]['gpu'])/float(m.clusterInfos[jj]['gpu-cap'])#test: (3-j)*0.15#
        geos[j]=m.clusterInfos[jj]['geolocation']
  
     
    xs=range(0,T)

    for j in range(M):  
        ax[j].clear()
        ax[j].axis([0, T, 0, 701])
        ax[j].set_xticks(ticks=range(5,T+1,5),labels=range(5,T+1,5),fontsize=5) #every 6 bars add label of slot
        ax[j].set_yticks(ticks=range(100,701,100),labels=range(100,701,100),fontsize=5)
        ax[j].set_ylabel('Carbon Intensity', fontsize = 8,labelpad=.4)
        ax[j].set_xlabel('Time Slots', fontsize = 8)
        ax[j].step(xs, carbonIntensity[j],color =colors_geos.get(geos[j]))
        ax[j].set_title(geos[j]+' ('+geos_full.get(geos[j])+') ', fontsize=10)

        ax[j+M].clear()
        ax[j+M].axis([0, T, 0, 110])
        ax[j+M].set_yticks(ticks=range(0,110,100),labels=range(0,110,100),fontsize=5)
        ax[j+M].set_xticks(ticks=range(5,T+1,5),labels=range(5,T+1,5),fontsize=5) #every 6 bars add label of slot
        ax[j+M].set_ylabel('GPU Allocation (%)', fontsize = 8,labelpad=.4)
        ax[j+M].set_xlabel('Time Slots', fontsize = 8)
        ax[j+M].bar(xs, utilization[j],color  =colors_geos.get(geos[j]))
        

ani1 = animation.FuncAnimation(fig, animate_cluster,interval=m.frequency*1000)       



def animate2(i):
    m.getAppWrappers()
    slow_down_ratio[i]=m.slow_down_metric
    lateness_ratio[i]=m.lateness_metric
    if i>0:
        carbon_metric[i]=carbon_metric[i-1]
        
    for j in range(M):
        carbon_metric[i]=carbon_metric[i]+(utilization[j][i] *carbonIntensity[j][i]/100)
        
    
    xs=range(0,T)

    for j in range(2):   
        
        ax2[j].clear()
        ax2[j].set_xticks(ticks=range(5,T+1,5),labels=range(5,T+1,5),fontsize=5) #every 6 bars add label of slot
        ax2[j].set_xlabel('Time Slots', fontsize = 8)
        if j==0:
            ax2[j].axis([0, T, 0, 30001])
            ax2[j].bar(xs, carbon_metric,color ='blue')
            ax2[j].set_yticks(ticks=range(0,30001,5000),labels=range(0,30001,5000),fontsize=5)
            ax2[j].set_ylabel('Carbon Measure', fontsize = 8)
       
        if j==1:
            ax2[j].axis([0, T, 0, 41])
            ax2[j].bar(xs, lateness_ratio,color ='blue')
            ax2[j].set_yticks(ticks=range(0,51,10),labels=range(0,51,10),fontsize=5)
            ax2[j].set_ylabel('Late Workloads (%)', fontsize = 8)
  
ani2 = animation.FuncAnimation(fig2, animate2,interval=m.frequency*1000)

plt.show()
    