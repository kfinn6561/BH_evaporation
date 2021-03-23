'''
Created on 27 Mar 2017

@author: Kieran Finn
'''
import pylab as p
import numpy as np
from general_tools import pdump
from root_numpy import root2array
import os
from colour_tools import kelly_colors

fig_dir='../plots/'
data_dir='conex_data'
files=os.listdir(data_dir)

kelly_colors=iter(kelly_colors)
kelly_colors=iter(['b','g','r','c','m','y','k'])
axes={}
colors={}
figs={}

for fname in files:
    if not fname.split('.')[-1]=='root':
        continue
    if fname[:5]=='no_cl':
        Ms=0
    else:
        Ms=float(fname.split('_')[1])
    if Ms not in colors.keys():
        colors[Ms]=next(kelly_colors)
    try:
        data=root2array(data_dir+'/'+fname,'Shower')
        E=list(data['lgE'])[0]
        if E in axes.keys():
            ax=axes[E]
        else:
            figs[E]=p.figure()
            p.title('E=%g'%E)
            ax=p.gca()
            axes[E]=ax
        for i in range(len(data['X'])):
            ax.plot(data['X'][i],data['N'][i],color=colors[Ms])
    except IOError:
        print 'Error reading %s no Shower data' %fname
        
for E in axes.keys():
    ax=axes[E]
    fig=figs[E]
    for Ms in np.sort(colors.keys()):
        ax.plot([],[],color=colors[Ms],label='Ms=%d'%Ms)
    ax.legend()
    fig.savefig(fig_dir+'profile_overlay_N_%.1f.pdf'%E)
p.show()
