'''
Created on 6 Apr 2017

@author: kieran
'''
import pylab as p
import numpy as np
from general_tools import pload

data=pload('convergence_data.pkl')
colours=['r','b','g','k']

xmax={}

ax1=p.subplot(211)
ax2=p.subplot(212,sharex=ax1)

for Ms in data.keys():
    for i in range(len(data[Ms]['lgE'])):
        E=data[Ms]['lgE'][i]
        xm=data[Ms]['Xmax'][i]
        label='M*=%d, log(E)=%.1f' %(Ms,E)
        if label not in xmax.keys():
            xmax[label]=[]
        xmax[label].append(xm)
        
labels=xmax.keys()
for i in range(len(labels)):
    label=labels[i]
    x=np.arange(len(xmax[label]))+1
    mean=[]
    median=[]
    std=[]
    for j in x:
        mean.append(np.mean(xmax[label][:j]))
        median.append(np.median(xmax[label][:j]))
        std.append(np.std(xmax[label][:j]))
    ax1.plot(x,mean,color=colours[i],label=label)
    ax1.plot(x,median,color=colours[i],ls='--')
    ax2.plot(x,std,color=colours[i])
    
ax1.plot([],[],color='k',label='mean')
ax1.plot([],[],color='k',ls='--',label='median')
ax1.set_title('Xmax')
ax2.set_title('RMS(Xmax)')

ax1.legend()
ax2.set_xlabel('number of showers')

p.show() 
    