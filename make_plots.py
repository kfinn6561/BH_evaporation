'''
Created on 27 Mar 2017

@author: Kieran Finn
'''
from general_tools import pload
import pylab as p
import numpy as np
from collections import defaultdict
from plot_functions import *
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


try:
    fname=sys.argv[1]
except IndexError:
    fname='xmax_data.pkl'



data=pload(fname)

plot_folder='../plots/'

if 'no_cl' in data.keys():
    data.pop('no_cl')

Frs=data.keys()
if 'forward' in Frs:
    Frs.remove('forward')

if no_cl:
    no_cl_data=pload('non_classicalized_data.pkl') 
else:
    no_cl_data=[]

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

Mc_colours={Mcs[i]:colours[i] for i in range(len(Mcs))}

Fr_colours={Frs[i]:colours[i] for i in range(len(Frs))}

default_Mc=170
default_Ms=100
default_Ms=50
default_Fr=100

'''Fraction Plot'''
if len(Frs):
    fig,axes=get_axes(no_cl_data)
    for Fr in Frs:
        plot_series(data[Fr][default_Ms][default_Mc],axes,Fr_colours[Fr],'%d%%' %Fr)
    
    axes[0].legend(ncol=3,loc='upper left',columnspacing=0.2,handletextpad=0.1,borderpad=0.1)
    axes[0].set_title('Fractional Dependence M*=%dGev, mu=%dMev' %(default_Ms, default_Mc))
    fig.savefig(plot_folder+'fractional_dependence.pdf')


'''Ms Plot'''
if len(Mss):
    fig,axes=get_axes(no_cl_data)
    for Ms in Mss:
        plot_series(data[default_Fr][Ms][default_Mc],axes,Ms_colours[Ms],'%dGeV' %Ms)
    
    axes[0].legend(ncol=3,loc='upper left',columnspacing=0.2,handletextpad=0.1,borderpad=0.1)
    axes[0].set_title('Threshold dependence f=%d%%, mu=%dMev' %(default_Fr, default_Mc))
    fig.savefig(plot_folder+'threshold_dependence.pdf')

'''Mc Plot'''
if len(Mcs):
    fig,axes=get_axes(no_cl_data)
    for Mc in Mcs:
        plot_series(data[default_Fr][default_Ms][Mc],axes,Mc_colours[Mc],'%dMeV' %Mc)
    
    axes[0].legend(ncol=3,loc='upper left',columnspacing=0.2,handletextpad=0.1,borderpad=0.1)
    axes[0].set_title('mu dependence f=%d%%, M*=%dGev' %(default_Fr, default_Ms))
    fig.savefig(plot_folder+'mu_dependence.pdf')

'''forward plot'''
if 'forward' in data.keys():
    thresholds=data['forward'].keys()
    threshold_colours={thresholds[i]:colours[i] for i in range(len(thresholds))}
    
    fig,axes=get_axes(no_cl_data)
    for threshold in thresholds:
        plot_series(data['forward'][threshold],axes,threshold_colours[threshold],"%d%%" %threshold)
    axes[0].legend(ncol=3,loc='upper left',columnspacing=0.2,handletextpad=0.1,borderpad=0.1)
    axes[0].set_title('forward resampling Xmax')
    fig.savefig(plot_folder+'forward_resampling.pdf')
    
    fig,axes=get_axes(no_cl_data,mu=True)
    for threshold in thresholds:
        plot_series(data['forward'][threshold],axes,threshold_colours[threshold],"%d%%" %threshold,xm='Xmumax')
    axes[0].legend(ncol=3,loc='upper left',columnspacing=0.2,handletextpad=0.1,borderpad=0.1)
    axes[0].set_title('forward resampling Xmumax')
    fig.savefig(plot_folder+'forward_resampling_mu.pdf')



p.show()
    