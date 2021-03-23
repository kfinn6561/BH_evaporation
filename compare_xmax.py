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

no_cl=True

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

PA_data=read_in_PA_data()

def plot_series(data,axes, Ms,Mc):
    ax_mean,ax_sigma=axes
    Es=data['lgE']
    xmax=data['Xmax']
    data_dict=defaultdict(list)
    for i in range(len(Es)):
        data_dict[Es[i]].append(xmax[i])
    sorted_Es=np.sort(data_dict.keys())
    mean=[]
    sigma=[]
    for E in sorted_Es:
        mean.append(np.mean(data_dict[E]))
        sigma.append(np.std(data_dict[E]))
    if Ms==0:
        lw=6
        color='k'
        ls='-'
    else:
        lw=3
        color=Ms_colours[Ms]
        ls=Mc_line_styles[Mc]
    ax_mean.plot(sorted_Es,mean,color=color,ls=ls,lw=lw)
    ax_sigma.plot(sorted_Es,sigma,color=color,ls=ls,lw=lw)

def get_axes(Fr):
    fig,axes=p.subplots(2,1,sharex=True,figsize=(18,12))
    ax_mean,ax_sigma=axes    
    ax_mean.set_title('%d%% Classicalization' %Fr)
    ax_sigma.set_xlabel('Log(E/eV)',fontsize=24)
    ax_mean.set_ylabel('Mean Xmax (g/cm^-2)',fontsize=24)
    ax_sigma.set_ylabel('RMS Xmax (g/cm^-2)',fontsize=24)
    
    for ax in axes:
        for Ms in Mss:
            ax.plot([],[],color=Ms_colours[Ms],lw=3,label='M*=%dGeV' %Ms)
        if no_cl:
            ax.plot([],[],color='k',lw=6,label='cl off')
        for Mc in Mcs:
            ax.plot([],[],color='k',lw=3,ls=Mc_line_styles[Mc],label='mu=%dMeV' %Mc)
    
    ax_mean.errorbar(PA_data['meanLgEnergy'],PA_data['meanXmax'],
                 yerr=[PA_data['meanXmaxSigmaSysUp']+PA_data['meanXmaxSigmaStat'],PA_data['meanXmaxSigmaStat']-PA_data['meanXmaxSigmaSysLow']],
                 fmt='o',color='k',ms=20,lw=6)
    ax_mean.legend(ncol=3,loc='lower right',columnspacing=0.2,handletextpad=0.1,borderpad=0.1)
    ax_mean.set_ylim(500,900)
        
        
    ax_sigma.errorbar(PA_data['meanLgEnergy'],PA_data['sigmaXmax'],
                 yerr=[PA_data['sigmaXmaxSigmaSysUp']+PA_data['sigmaXmaxSigmaStat'],PA_data['sigmaXmaxSigmaStat']-PA_data['sigmaXmaxSigmaSysLow']],
                 fmt='o',color='k',ms=20,lw=6)
    #ax_sigma.legend(ncol=2,loc='upper right',columnspacing=0.2,handletextpad=0.1,borderpad=0.1)
    ax_sigma.set_ylim(20,85)
    
    ax_sigma.set_xlim(17.8,20)
    return (fig,axes)


try:
    fname=sys.argv[1]
except IndexError:
    fname='xmax_data.pkl'



data=pload(fname)

plot_folder='../plots/'

if 'no_cl' in data.keys():
    data.pop('no_cl')

Frs=data.keys()
if no_cl:
    data['no_cl']=pload('non_classicalized_data.pkl') 

Frs=np.sort(Frs)
Mss=[]
Mcs=[]
for Fr in Frs:
    for Ms in data[Fr].keys():
        Mss.append(Ms)
        for Mc in data[Fr][Ms].keys():
            Mcs.append(Mc)
Mss=np.sort(list(set(Mss)))
Mcs=np.sort(list(set(Mcs)))

colours=colour_tools.kelly_colors
Ms_colours={Mss[i]:colours[i] for i in range(len(Mss))}

line_styles=['-','--','-.',':']
Mc_line_styles={Mcs[i]:line_styles[i] for i in range(len(Mcs))}

for Fr in Frs:    
    full_fig,full_axes=get_axes(Fr)
    
    
    for Ms in data[Fr].keys():
        Ms_fig,Ms_axes=get_axes(Fr)
        for Mc in data[Fr][Ms].keys():
            plot_series(data[Fr][Ms][Mc],full_axes,Ms,Mc)
            plot_series(data[Fr][Ms][Mc],Ms_axes,Ms,Mc)
            
        if no_cl:
            plot_series(data['no_cl'],Ms_axes,0,0)
        Ms_fig.savefig(plot_folder+'compare_xmax_%02d_%d.png' %(Fr,Ms))
            
    if no_cl:
            plot_series(data['no_cl'],full_axes,0,0)
            
    full_fig.savefig(plot_folder+'compare_xmax_%02d.png' %Fr)
p.show()
    