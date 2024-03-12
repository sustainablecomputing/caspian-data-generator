
import math
import random
from dateutil import parser
from matplotlib.patches import Rectangle
import pylab as pl
import sys
import kubernetes
from kubernetes.config import kube_config
import collections
from kubernetes.client.rest import ApiException
import numpy as np
collections.Callable = collections.abc.Callable
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import PercentFormatter

total_jobs=173
# Monitoring: - retrieve the specs of clusterinfo objects in the hub and plot the info
class Monitoring(object):
    contxt="k3d-hub"
    kube_config="~/.kube/config"   
    
    api_client=None
    api_instance=None

    frequency=1                # frequency of updating the plot (every 60 seconds)
    
    clusterInfos=[]             # clusterInfo objects in the hub
    T=45                   # number of time slots. Each slot is 6*60 seconds
    slow_down_metric=0                      #number of bars  per slot to display  
    lateness_metric=0
    late_percentage=0
    num_late=0
    M=3   
    num_bin=40
    ratio_val=[]
    max_val=2
    min_val=0
    
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
                slope=(int(ci['spec']['powerpeak'])-int(ci['spec']['poweridle']))/100.0
                   
                if 'usage' in ci['status'] and 'nvidia.com/gpu' in ci['status']['usage']:
                    tmp = {'slope':slope,'geolocation':ci['spec']['geolocation'],'name':ci['metadata']['name'],'gpu':ci['status']['usage']['nvidia.com/gpu'],'gpu-cap':ci['status']['capacity']['nvidia.com/gpu'],'carbon': ci['spec']['carbon']}
                else:
                   tmp = {'slope':slope,'geolocation':ci['spec']['geolocation'], 'name':ci['metadata']['name'],'gpu':'0','gpu-cap':ci['status']['capacity']['nvidia.com/gpu'],'carbon': ci['spec']['carbon']}
               
                self.clusterInfos.append(tmp)    
                #print(tmp['slope'], tmp['geolocation'])                     
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
        self.num_per_bin=[0]*self.num_bin
        self.ratio_val=[]
        #date_format = '%Y-%m-%dT %H:%M:%SZ'
        latenessTime=0
      
        
        try:
            api_response = self.api_instance.list_cluster_custom_object( group, version, plural,timeout_seconds=2,   watch=False)
            aws=api_response.get('items')           
            
            for aw in aws:
                
                TimeDispatched=0
               # print(aw['metadata']['name']) 
                if  'dispatcherStatus' in aw['spec'] and (aw['spec']['dispatcherStatus']['phase']== "Succeeded")or (aw['spec']['dispatcherStatus']['phase']== "Queued" and 'timeDispatched' in aw['spec']['dispatcherStatus'] and  int(aw['spec']['dispatcherStatus']['timeDispatched'])>(int(aw['spec']['sustainable']['runTime']))):#3*self.frequency+
                 
                  lenn = len(aw['spec']['dispatcherStatus']['transitions'])
                  responseTime= (parser.parse (aw['spec']['dispatcherStatus']['transitions'][lenn-1]['time'])- parser.parse (aw['metadata']['creationTimestamp'])).total_seconds()
                  deadline=(parser.parse (aw['spec']['sustainable']['deadline'])- parser.parse (aw['metadata']['creationTimestamp'])).total_seconds()+self.frequency*1
                
                  latenessTime= (parser.parse (aw['spec']['dispatcherStatus']['transitions'][lenn-1]['time'])- parser.parse (aw['spec']['sustainable']['deadline'])).total_seconds()-self.frequency*2
                 
                  avg_slowdown+=(responseTime/int(aw['spec']['sustainable']['runTime']))
                  if latenessTime>0:
                    avg_lateness+=(latenessTime/self.frequency)
                    num_late+=1

                
            
                  num_succeed+=1
                  ratio=responseTime/deadline
                  self.ratio_val.append(ratio)
                  bin_ind=int(m.num_bin*ratio/(m.max_val-m.min_val))
                  bin_ind=min(m.num_bin-1,bin_ind)
                  m.num_per_bin[bin_ind]+=1
               
                 
            if num_succeed>0:
                m.slow_down_metric=avg_slowdown/(num_succeed)
                m.lateness_metric=100*num_late/num_succeed#avg_lateness/num_succeed
                print("ppp", sum(self.ratio_val)/num_succeed)
            #print('kk',num_succeed,avg_slowdown/(num_succeed),avg_lateness/num_succeed)
		                                   
        except ApiException as e:
            print("Exception when calling CustomObjectsApi->get_cluster_custom_object: %s\n" % e)

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
hub_context="k3d-hub"
frequency=1
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

carbonIntensity=[[None for i in range(T)] for j in range(M)]

carbon_metric=[None]*T
lateness_ratio=[0]*T
slow_down_ratio=[0]*T
ax=[]
ax2=[]

fig = plt.figure("Cluster Performance",figsize=(9,5.8))
fig2 = plt.figure("Overall Performance",figsize=(9,3.5))


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
colors_geos={'CA-ON':'green','DE':'red', 'JP-KN':'orange'}
positions={}
fix_position={'CA-ON':0, 'DE':2 ,'JP-KN':1}
slopes=[1, 1 ,1]
for j in range(M):
    positions.update({m.clusterInfos[j]['geolocation']:j})

def animate_cluster(i):
    m.get_clusterInfos()
    for jj in range(M):
        j= positions.get(m.clusterInfos[jj]['geolocation'])
    
        carbonIntensity[j][i]=int(m.clusterInfos[jj]['carbon'][0])#dframe.iloc[int(t/m.perSlot)][zones[j]]
        utilization[j][i]=100*float(m.clusterInfos[jj]['gpu'])/float(m.clusterInfos[jj]['gpu-cap'])#test: (3-j)*0.15#
        geos[j]=m.clusterInfos[jj]['geolocation']
        slopes[j]=m.clusterInfos[jj]['slope']
     
    xs=range(0,T)

    for j in range(M):  
        jj= fix_position.get(geos[j])
        ax[jj].clear()
        ax[jj].axis([0, T, 0, 701])
        ax[jj].set_xticks(ticks=range(5,T+1,5),labels=range(5,T+1,5),fontsize=6) #every 6 bars add label of slot
        ax[jj].set_yticks(ticks=range(100,701,100),labels=range(100,701,100),fontsize=6)
        ax[jj].set_ylabel('Carbon Intensity', fontsize = 8,labelpad=.4)
        ax[jj].set_xlabel('Time Slots', fontsize = 8)
        ax[jj].step(xs, carbonIntensity[j],color =colors_geos.get(geos[j]))
        ax[jj].set_title(geos[j]+' ('+geos_full.get(geos[j])+') ', fontsize=10)

        ax[jj+M].clear()
        ax[jj+M].axis([0, T, 0, 110])
        ax[jj+M].set_yticks(ticks=range(0,110,100),labels=range(0,110,100),fontsize=6)
        ax[jj+M].set_xticks(ticks=range(5,T+1,5),labels=range(5,T+1,5),fontsize=6) #every 6 bars add label of slot
        ax[jj+M].set_ylabel('GPU Allocation (%)', fontsize = 8,labelpad=.4)
        ax[jj+M].set_xlabel('Time Slots', fontsize = 8)
        ax[jj+M].bar(xs, utilization[j],color  =colors_geos.get(geos[j]))
        ax[1].get_figure().savefig('./fig/clusters'+str(i)+'.pdf')

ani1 = animation.FuncAnimation(fig, animate_cluster,interval=m.frequency*1000)       


def animate2(i):
    m.getAppWrappers()
    slow_down_ratio[i]=m.slow_down_metric
    lateness_ratio[i]=m.lateness_metric
    carbon_metric[i]=0
    if i>0:
        carbon_metric[i]=carbon_metric[i-1]
         
    for j in range(M):

        carbon_metric[i]=carbon_metric[i]+( slopes[j]*utilization[j][i] *carbonIntensity[j][i]/100)#test:1000*(np.random.randint(0,4))+
        
    
    xs=range(0,T)
   
    ax2[0].clear()
    ax2[0].set_xticks(ticks=range(5,T+1,5),labels=range(5,T+1,5),fontsize=6) #every 6 bars add label of slot
    ax2[0].set_xlabel('Time Slots', fontsize = 8)
    ax2[0].axis([0, T, 0, 50001])
    ax2[0].plot(xs, carbon_metric,marker='.',color ='#607c8e')
    ax2[0].set_yticks(ticks=range(0,50001,10000),labels=range(0,50001,10000),fontsize=6)
    ax2[0].set_ylabel('Carbon Measure', fontsize = 8)
   
    if len(m.ratio_val)>0:
        ax2[1].clear()
        ax2[1].set_ylabel('Percentage of Jobs', fontsize = 8)
       # my_hist, bin_edges = np.histogram(m.ratio_val, bins=m.num_bin,weights=np.ones(len(m.ratio_val)) / len(m.ratio_val))
        #my_hist=m.num_per_bin/(sum(m.num_per_bin))
        my_hist = [x /(total_jobs) for x in m.num_per_bin]
        bin_edges=[0]*(m.num_bin+1)
        for i in range(m.num_bin+1):
            bin_edges[i]=i*(m.max_val-m.min_val)/m.num_bin

      
        labels= ["On Time ($\\alpha ≤1$)","Late ($1<\\alpha ≤1.2$)", "Very Late ($\\alpha >1.2$)"]
        cmap = plt.get_cmap('RdYlBu_r')
        low = cmap(0.5)
        medium =cmap(0.25)
        high = cmap(0.8)
        lower_bound = 1#min(m.ratio_val)
        upper_bound = 1.2#max(m.ratio_val)

# Define colors for tails and center
        lower_tail_color =low# "lightblue"
        hist_center_color = medium#"lightcoral"
        upper_tail_color = high#"lightcoral"
    
# Init the list containing the color of each bin.
        colors = []

        for bin_edge in bin_edges:
    
    # Light blue: Assign a color to the bin if its edge is less than 'lower_bound'
            if bin_edge <= lower_bound:
                colors.append(lower_tail_color)
    
    # Dark gray: Assign a color to the bin if its edge is greater than or equal to 'upper_bound'
            elif bin_edge > upper_bound:
                colors.append(upper_tail_color)  
    
    # Purple: Assign a color to the bin if its edge is between -10 and 10
            else:
            
                colors.append(hist_center_color)
            # Create a bar plot with specified colors and bin edges
            ax2[1].bar(
            bin_edges[:-1], 
            my_hist, 
            width=np.diff(bin_edges), 
            color=colors, 
            edgecolor='gray'
    ) 
        
        plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
        ax2[1].axis([0, m.max_val, 0, .31])
        ax2[1].set_xlabel('$\\alpha$ :Job Completion Time Ratio', fontsize = 8)
        ax2[1].tick_params(axis='x', labelsize=6)
        ax2[1].tick_params(axis='y', labelsize=6)
        ax2[1].set_yticks(np.arange(0, .31, .1))

        handles = [Rectangle((0,0),1,1,color=c,ec="k") for c in [low,medium, high]]

        plt.legend(handles, labels, fontsize = 7)
        
        ax2[1].get_figure().savefig('./fig/overall'+str(i)+'.pdf')
       # ax2[1].set_xticks(bb[0:10],labels=bb[0:m.num_bin])
ani2 = animation.FuncAnimation(fig2, animate2,interval=m.frequency*1000)

plt.show()

    