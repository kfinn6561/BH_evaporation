'''
Created on 19 Mar 2017

@author: Kieran Finn
'''
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


mu0=0.5#mass of the emitted particle
Mthreshold=1000.#planck mass, GeV

def calc_N(M,Ms=Mthreshold,mu=mu0):
    return (M/mu)*lambertw(M*mu/(Ms**2)).real

def calc_old_N(M,Ms=Mthreshold):
    return (M**2)/(Ms**2)

def flip(items, ncol):
    return itertools.chain(*[items[i::ncol] for i in range(ncol)])


Mss=10.**np.arange(0,4)
Es=np.logspace(2,6.5)

p.figure()

for i in range(len(Mss)):
    Ms=Mss[i]
    old_Ns=calc_old_N(Es,Ms)
    p.plot(Es,old_Ns,color=kelly_colors[i+2],ls='dotted')

for i in range(len(Mss)):
    Ms=Mss[i]
    mid_Ns=calc_N(Es,Ms,mu=0.17)
    p.plot(Es,mid_Ns,color=kelly_colors[i+2],ls='dashdot')
    
for i in range(len(Mss)):
    Ms=Mss[i]
    Ns=calc_N(Es,Ms)
    p.plot(Es,Ns,color=kelly_colors[i+2],label="M*=%gGeV" %Ms,lw=4)

    
#p.plot(Es,Es/0.5,color='k',label='mu=500MeV',lw=6)
p.plot(Es,Es/0.17,color='k',ls='dashdot',lw=4)

    
p.plot([],[],color='k',label='mu=500MeV',lw=4)
p.plot([],[],color='k',ls='dashdot',label='mu=170MeV')
p.plot([],[],color='k',ls='dotted',label='mu=0')

p.fill_between(Es,Es/0.5,1e8,color='k',alpha=0.2,label='N*mu>M')

    
p.loglog()
p.xlim(Es[0],Es[-1])
p.ylim(100,1e8)

p.xlabel('Centre of Mass Energy (GeV)',fontsize=24)
p.ylabel('Number of particles',fontsize=24)

ax=p.gca()

handles, labels = ax.get_legend_handles_labels()
#p.legend(flip(handles, 3), flip(labels, 3),loc='upper left',ncol=3,mode='expand')
nlines=len(Mss)
legend1=p.legend(handles[:nlines],labels[:nlines],loc='upper left')
p.legend(handles[nlines:],labels[nlines:],loc='lower right')
ax.add_artist(legend1)


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

p.show()


