'''
Created on 19 Mar 2017

@author: Kieran Finn
'''
import pylab as p
import numpy as np
from scipy.special import lambertw
from colour_tools import kelly_colors
import matplotlib as mpl
import itertools

mpl.rcParams.update({'font.size': 24})
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



mb2gev=0.3893793

sigrange=np.array([200,650])/mb2gev#convert to GeV^-2


mu0=0.5#mass of the emitted particle
Mthreshold=1000.#planck mass, GeV

def calc_N(M,Ms=Mthreshold,N0=1.,mu=mu0):
    return N0*(M/mu)*lambertw(M*mu/(Ms**2)).real
def calc_M(N,Ms=Mthreshold,N0=1.,mu=mu0):
    return mu*(N/N0)/lambertw(np.sqrt(N/N0)*mu/(2*Ms)).real
def calc_sig(M,Ms=Mthreshold,mu=mu0):
    return (np.pi*(lambertw(M*mu/(Ms**2))/mu)**2).real


def calc_old_sig(M,Ms=Mthreshold):
    return np.pi*(M/(Ms**2))**2

def flip(items, ncol):
    return itertools.chain(*[items[i::ncol] for i in range(ncol)])

Mss=10.**np.arange(-2,4)
Es=np.logspace(0,6.5)

p.figure()
p.plot([],[],color='k',label='mu=500MeV')
p.plot([],[],color='k',ls='dashdot',label='mu=170MeV')
p.plot([],[],color='k',ls='dotted',label='mu=0')
    
for i in range(len(Mss)):
    Ms=Mss[i]
    old_sigs=calc_old_sig(Es,Ms)
    p.plot(Es,old_sigs,color=kelly_colors[i],ls='dotted')
    
for i in range(len(Mss)):
    Ms=Mss[i]
    mid_sigs=calc_sig(Es,Ms,mu=0.17)
    p.plot(Es,mid_sigs,color=kelly_colors[i],ls='dashdot')
    
for i in range(len(Mss)):
    Ms=Mss[i]
    sigs=calc_sig(Es,Ms)
    p.plot(Es,sigs,color=kelly_colors[i],label="M*=%gGeV" %Ms,lw=4)
    

    
   
p.fill_between(Es,sigrange[0],sigrange[1],color='r',alpha=0.3)
p.loglog()
p.xlim(Es[0],Es[-1])
p.ylim(0.1,1e4)

p.xlabel('Centre of Mass Energy (GeV)',fontsize=24)
p.ylabel('Cross Section (GeV^-2)',fontsize=24)

ax=p.gca()

handles, labels = ax.get_legend_handles_labels()
p.legend(flip(handles, 3), flip(labels, 3),loc='lower left',ncol=3,mode='expand')

textlabel='Range of normal\ncross sections'
gmean=np.sqrt(sigrange[0]*sigrange[1])
p.text(2,gmean,textlabel,color='white',bbox=dict(facecolor='white'),verticalalignment='center')
p.text(2,gmean,textlabel,bbox=dict(facecolor='red',alpha=0.3),verticalalignment='center')



axx=ax.twiny()
lims=np.array(ax.get_xlim())
axx.set_xscale('log')
axx.set_xlim(lims[0],lims[1])
lims=1e9*(lims**2)/(2*0.94)
logticklims=np.ceil(np.log10(lims))
xticklabels=np.arange(int(logticklims[0]),(logticklims[1]))
xtickpos=np.sqrt(2*((10.**xticklabels)/1e9)*0.94)
xtickLabels=['$\mathregular{10^{%d}}$' %i for i in xticklabels]
axx.set_xticks(xtickpos)
axx.set_xticklabels(xtickLabels)
axx.minorticks_off()
axx.set_xlabel('Lab Energy (eV)',fontsize=24)

axy=ax.twinx()
lims=np.array(ax.get_ylim())
lims=lims*mb2gev
axy.set_yscale('log')
axy.set_ylim(lims[0],lims[1])
axy.set_ylabel('mb', fontsize=24)

p.show()


