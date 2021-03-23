'''
Created on 27 Mar 2017

@author: Kieran Finn
'''
import pylab as p
import numpy as np
from general_tools import pdump
from root_numpy import root2array
import os

data_dir='conex_data'
outname='xmax_data.pkl'
files=os.listdir(data_dir)

data={}
errors=0
no_files=len(files)

for fname in files:
    if not fname.split('.')[-1]=='root':
        continue
    if fname[:5]=='no_cl':
        Ms=0
    else:
        Ms=float(fname.split('_')[1])
    if Ms not in data.keys():
        data[Ms]={'lgE':[],'Xmax':[]}
    try:
        dd=root2array(data_dir+'/'+fname,'Shower')
        data[Ms]['lgE']+=list(dd['lgE'])
        data[Ms]['Xmax']+=list(dd['Xmax'])
    except IOError:
        print 'Error reading %s no Shower data' %fname
        errors+=1
print 'total files: %d' %no_files
print 'total errors: %d. %.2f percent of files' %(errors, 100.*float(errors)/float(no_files))
pdump(data,outname)
