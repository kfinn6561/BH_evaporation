'''
Created on 27 Mar 2017

@author: Kieran Finn
'''
from general_tools import pload
import pylab as p
import numpy as np
from collections import defaultdict
import colour_tools
import sys

import matplotlib as mpl
mpl.rcParams.update({'font.size': 22})
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times']#Computer Modern Roman']
#mpl.rcParams['font.weight'] = 'bold'
mpl.rcParams['axes.labelsize'] = 20
mpl.rcParams['xtick.labelsize'] = 24.
mpl.rcParams['ytick.labelsize'] = 24.
mpl.rcParams['xtick.major.size']= 10.
mpl.rcParams['xtick.minor.size']= 5.
mpl.rcParams['ytick.major.size']= 10.
mpl.rcParams['ytick.minor.size']= 5.
mpl.rcParams['figure.max_open_warning']=False
mpl.rcParams['lines.linewidth']=2


def read_in_PA_data(fname='../Data/PA_xmax_data/xmaxMoments.txt'):
    f=open(fname,'r')
    r=f.readlines()
    f.close()
    headers=['energyBin','lgMinEnergy','lgMaxEnergy','meanLgEnergy','numberOfEvents',
             'meanXmax','meanXmaxSigmaStat','meanXmaxSigmaSysUp','meanXmaxSigmaSysLow',
             'sigmaXmax','sigmaXmaxSigmaStat','sigmaXmaxSigmaSysUp','sigmaXmaxSigmaSysLow']
    out={header:[] for header in headers}
    for line in r:
        numbers=line.split()
        for i in range(len(headers)):
            out[headers[i]].append(float(numbers[i]))
    for header in headers:
        out[header]=np.array(out[header])
    return out


try:
    fname=sys.argv[1]
except IndexError:
    fname='xmax_data.pkl'



data=pload(fname)
p.figure()
#p.title('Overlapping Spheres')
p.xlabel('Log(E/eV)',fontsize=24)
p.ylabel('Median Xmax (g/cm^-2)',fontsize=24)
ax_mdn=p.gca()

p.figure()
#p.title('Overlapping Spheres')
p.xlabel('Log(E/eV)',fontsize=24)
p.ylabel('Mean Xmax (g/cm^-2)',fontsize=24)
ax_mean=p.gca()

p.figure()
#p.title('Overlapping Spheres')
p.xlabel('Log(E/eV)',fontsize=24)
p.ylabel('RMS Xmax (g/cm^-2)',fontsize=24)
ax_sigma=p.gca()

axes=[ax_mdn,ax_mean,ax_sigma]

Mss=np.sort(data.keys())
Mss=np.roll(Mss,-1)
#colours=colour_tools.linear_gradient('#ff0000','#0000ff',n=len(Mss)-1)['hex']
colours=colour_tools.kelly_colors
Ms_colours={Mss[i]:colours[i] for i in range(len(Mss)-1)}
for Ms in Mss:
    p.figure()
    Es=data[Ms]['lgE']
    xmax=data[Ms]['Xmax']
    p.scatter(Es,xmax)
    data_dict=defaultdict(list)
    for i in range(len(Es)):
        data_dict[Es[i]].append(xmax[i])
    sorted_Es=np.sort(data_dict.keys())
    mdn=[]
    mean=[]
    sigma=[]
    lq=[]
    uq=[]
    for E in sorted_Es:
        mdn.append(np.median(data_dict[E]))
        mean.append(np.mean(data_dict[E]))
        sigma.append(np.std(data_dict[E]))
        lq.append(np.percentile(data_dict[E],25))
        uq.append(np.percentile(data_dict[E],75))
    p.plot(sorted_Es,mdn)
    p.fill_between(sorted_Es, lq,uq, alpha=0.3)
    p.title('M*=%g' %Ms)
    p.xlabel('Log(E/eV)',fontsize=24)
    p.ylabel('Xmax (g/cm^-2)',fontsize=24)
    if Ms==0:
        ax_mdn.plot(sorted_Es,mdn,color='k',lw=6,label='cl off')
        ax_mean.plot(sorted_Es,mean,color='k',lw=6,label='cl off')
        ax_sigma.plot(sorted_Es,sigma,color='k',lw=6,label='cl off')
    else:
        ax_mdn.plot(sorted_Es,mdn,color=Ms_colours[Ms],lw=3,label='M*=%gGeV' %Ms)
        ax_mean.plot(sorted_Es,mean,color=Ms_colours[Ms],lw=3,label='M*=%gGeV' %Ms)
        ax_sigma.plot(sorted_Es,sigma,color=Ms_colours[Ms],lw=3,label='M*=%gGeV' %Ms)
    
PA_data=read_in_PA_data()

for ax in [ax_mdn, ax_mean]:
    ax.errorbar(PA_data['meanLgEnergy'],PA_data['meanXmax'],
                 yerr=[PA_data['meanXmaxSigmaSysUp'],-PA_data['meanXmaxSigmaSysLow']],
                 fmt='o',color='k',ms=20,lw=6)
    ax.legend(ncol=2,loc='lower right',columnspacing=0.2,handletextpad=0.1,borderpad=0.1)
    ax.set_ylim(500,900)
    
    
ax_sigma.errorbar(PA_data['meanLgEnergy'],PA_data['sigmaXmax'],
             yerr=[PA_data['sigmaXmaxSigmaSysUp'],-PA_data['sigmaXmaxSigmaSysLow']],
             fmt='o',color='k',ms=20,lw=6)
ax_sigma.legend(ncol=2,loc='upper right',columnspacing=0.2,handletextpad=0.1,borderpad=0.1)
ax_sigma.set_ylim(20,180)


for ax in axes:
    ax.set_xlim(18,20)
p.show()
    