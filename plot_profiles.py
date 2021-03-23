'''
Created on 27 Mar 2017

@author: Kieran Finn
'''
import pylab as p
import numpy as np
from general_tools import pdump
from root_numpy import root2array
import os

data_dir='../Data/First_run'
files=os.listdir(data_dir)

axes={}

for fname in files:
    if not fname.split('.')[-1]=='root':
        continue
    if fname[:5]=='no_cl':
        Ms=0
    else:
        Ms=float(fname.split('_')[1])
    if Ms not in axes.keys():
        axes[Ms]={}
    try:
        data=root2array(data_dir+'/'+fname,'Shower')
        E=list(data['lgE'])[0]
        if E in axes[Ms].keys():
            ax=axes[Ms][E]
        else:
            p.figure()
            p.title('Ms=%d, E=%g'%(Ms,E))
            ax=p.gca()
            axes[Ms][E]=ax
        for i in range(len(data['X'])):
            ax.plot(data['X'][i],data['dEdX'][i])
    except IOError:
        print 'Error reading %s no Shower data' %fname
        
p.show()