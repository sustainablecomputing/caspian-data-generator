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
   
    kube_config="~/.kube/config"   
    contxt="k3d-hub"
    api_client=None
    api_instance=None
    frequency=10                # frequency of updating the plot (every 10 seconds)
    
    clusterInfos=[]             # clusterInfo objects in the hub
    Slots=36                     # number of time slots. Each slot is 6*10 seconds
    perSlot=6                      #number of bars  per slot to display
    T=36*6                      #number of bars in the plot (to visualize system over 36*6*10 seconds)
    
    M=3                         # number of available clusterinfo (default value is 3)
 
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
# create client to talk to the hub
    def __init__(self):         
        self.api_client=kube_config.new_client_from_config(config_file=self.kube_config,context=self.contxt)
        self.api_instance = kubernetes.client.CustomObjectsApi(self.api_client)

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
                print(ci['metadata']['name']) 
                if 'usage' in ci['status'] and 'nvidia.com/gpu' in ci['status']['usage']:
                    tmp = { 'name':ci['metadata']['name'],'gpu':ci['status']['usage']['nvidia.com/gpu'],'gpu-cap':ci['status']['capacity']['nvidia.com/gpu'],'carbon': ci['spec']['carbon']}
                else:
                   tmp = { 'name':ci['metadata']['name'],'gpu':'0','gpu-cap':ci['status']['capacity']['nvidia.com/gpu'],'carbon': ci['spec']['carbon']}
                
                self.clusterInfos.append(tmp)                                 
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
m=Monitoring()
T=m.T
M=m.M


utilization= [[0 for i in range(T)] for j in range(M)]
em_rate=[0]*T
#slow_down: for test
slow_down=[1,1,1,1.2,1.2,1.4,1.4,1.3,1.4,1.5,1.4,1.5,1.6,1.5,1.5,1.6,1.6,1.7,1.7,1.5,1.7,1.6,1.7,1.6,1.5,1.6,1.5,1.5,1.6,1.6,1.7,1.7,1.5,1.5,1.6,1.5]
b_slow_down=[1,1,1,1.2,1.2,1,1.1,1.1,1.3,1.3,1.2,1.2,1.3,1.3,1.1,1.1,1.2,1.7,1.2,1.5,1.7,1.1,1.4,1.6,1.5,1.1,1.1,1.3,1.2,1.3,1.2,1.4,1.1,1.5,1.2,1.2]

zones=[ 'CA-ON','US-NY','GB']
dframe=pd.read_csv('./data/CI.csv', usecols= ['timestamp', 'CA-ON','US-NY','GB'])
carbon=[]
carbonIntensity=[[0 for i in range(T)] for j in range(M)]

aggrigaetd_em_sust=[0]*T
aggrigaetd_em_qos=[0]*T
b_slow_down_ratio=[0]*T
slow_down_ratio=[0]*T
ax=[]
colors=['green','red', 'brown']
fig = plt.figure(figsize=(17,10))
for j in range(M):
    ax.append(fig.add_subplot(3,M,j+1))

for j in range(M):
 ax.append(fig.add_subplot(3,M,j+M+1))

for j in range(M):
 ax.append(fig.add_subplot(3,M,j+2*M+1))

def animate(i):
    slow_down_ratio[i]=slow_down[int(i/m.perSlot)]
    b_slow_down_ratio[i]=b_slow_down[int(i/m.perSlot)]
    for j in range(M):
        for t in range(i,m.perSlot*24+i):
            if t<T:
                carbonIntensity[j][t]=dframe.iloc[int(t/m.perSlot)][zones[j]]
       
    if i>0:
        aggrigaetd_em_sust[i]=aggrigaetd_em_sust[i-1]
        aggrigaetd_em_qos[i]=aggrigaetd_em_qos[i-1]
    m.get_clusterInfos()
    aggrigaetd_load=0
    for j in range(M):
        utilization[j][i]=(3-j)*0.15#float(m.clusterInfos[0]['gpu'])/float(m.clusterInfos[0]['gpu-cap'])
        aggrigaetd_load=aggrigaetd_load+utilization[j][i]
        aggrigaetd_em_sust[i]=aggrigaetd_em_sust[i]+(utilization[j][i] *carbonIntensity[j][i])
        
    
    avg_carbon=0
    for j in range(M):
        avg_carbon = avg_carbon+carbonIntensity[j][i]
    
    aggrigaetd_em_qos[i]=aggrigaetd_em_qos[i]+(aggrigaetd_load*avg_carbon/float(M))
    
    em_rate[i]=100*(aggrigaetd_em_qos[i]-aggrigaetd_em_sust[i])/aggrigaetd_em_qos[i]
    xs=range(0,int(T))

    for j in range(M):
        
        ax[j].clear()
        ax[j].axis([0, T, 0, 300.1])
        ax[j].set_xticks(ticks=range(0,int(T),int(T/m.Slots)),labels=range(0,m.Slots,1),fontsize=5) #every 6 bars add label of slot
        ax[j].set_yticks(ticks=range(0,400,50),labels=range(0,400,50),fontsize=5)
        ax[j].set_ylabel('Carbon Intensity', fontsize = 6)
        ax[j].set_xlabel('Time slots', fontsize = 6)
        ax[j].step(xs, carbonIntensity[j],color =colors[j])
        ax[j].set_title('Spoke '+ str(j+1), fontsize=6)

        ax[j+M].clear()
        ax[j+M].axis([0, T, 0, 1.1])
        ax[j+M].set_yticks(ticks=range(0,2),labels=range(0,2,1),fontsize=5)
        ax[j+M].set_xticks(ticks=range(1,int(T),int(T/m.Slots)),labels=range(1,m.Slots+1,1),fontsize=5) #every 6 bars add label of slot 
        ax[j+M].set_ylabel('GPU utilization', fontsize = 6)
        ax[j+M].set_xlabel('Time slots', fontsize = 6)
        ax[j+M].bar(xs, utilization[j],color =colors[j])
        ax[j+M].set_title('spoke '+ str(j+1), fontsize=6)

        ax[j+2*M].clear()
        ax[j+2*M].set_xticks(ticks=range(0,int(T),int(T/m.Slots)),labels=range(0,m.Slots,1),fontsize=5) #every 6 bars add label of slot
        ax[j+2*M].set_xlabel('Time slots', fontsize = 6)
        if j==0:
            ax[j+2*M].axis([0, T, 0, 100.1])
            ax[j+2*M].bar(xs, em_rate,color ='blue')
            ax[j+2*M].set_yticks(ticks=range(0,100,50),labels=range(0,100,50),fontsize=5)
            ax[j+2*M].set_ylabel('Carbon Reduction rate', fontsize = 6)
        if j==1:
            ax[j+2*M].axis([0, T, 0, 3.1])
            ax[j+2*M].bar(xs, slow_down_ratio,color ='blue')
            ax[j+2*M].set_yticks(ticks=range(0,3,1),labels=range(0,3,1),fontsize=5)
            ax[j+2*M].set_ylabel('Slow down', fontsize = 6)
        
        if j==2:
            ax[j+2*M].axis([0, T, 0, 3.1])
            ax[j+2*M].bar(xs, b_slow_down_ratio,color ='blue')
            ax[j+2*M].set_yticks(ticks=range(0,3,1),labels=range(0,3,1),fontsize=5)
            ax[j+2*M].set_ylabel('Bouded Slow down', fontsize = 6)
        

if __name__ == '__main__':
    
    ani = animation.FuncAnimation(fig, animate,interval=m.frequency*1000)
    plt.show()
    