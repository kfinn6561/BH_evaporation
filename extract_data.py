'''
Created on 27 Mar 2017

@author: Kieran Finn
'''
import pylab as p
import numpy as np
from general_tools import pdump
from root_numpy import root2array
import os

'''
Created on 25 May 2016

@author: kieran
'''
import numpy as np
import pylab as p
from scipy.optimize import curve_fit
from scipy.stats import halfnorm
from general_tools import pload,pdump,progress_bar
from scipy.interpolate import interp1d
from copy import copy
#from multiprocessing import Pool


rho=0.001275#g/cm^3 density of air
X0=36.62#g/cm^2
lambda_N=80.#g/cm^2
Ec=0.086#GeV
c=3e10#cm/s

def GH_fit(x,N,X1,xm,l):
    return np.nan_to_num(N*np.power((x-X1)/(xm-X1),(xm-X1)/l)* np.exp((xm-x)/l))

def find_fit(x,y,verbose=False):
    i=np.argmax(y)
    x1=0.
    xm=x[i]
    n=y[i]
    l=lambda_N
    try:
        return curve_fit(GH_fit,x,y,p0=[n,x1,xm,l],sigma=0.1*y+1.)
    except RuntimeError:
        print 'Failure fitting curve, returning maximum value'
        return ([n,x1,xm,l],'fail')

def get_mu_max(data):
    out=[]
    for i in range(len(data)):
        popt,_=find_fit(data[i]['X'],data[i]['dMu'])
        out.append(popt[2])
    return out

data_dir=os.environ['HOME']+'/conex_data'
outname='xmax_data.pkl'
files=os.listdir(data_dir)

data={}
errors=0
no_files=len(files)

for fname in files:
    if not fname.split('.')[-1]=='root':
        continue
    if fname[:5]=='no_cl':
        if 'no_cl' not in data.keys():
            data['no_cl']={'lgE':[],'Xmax':[],'Xmumax':[]}
        to_update=data['no_cl']
        
    elif fname[:7]=='forward':
        if 'forward' not in data.keys():
            data['forward']={}
        FT=int(fname.split('_')[1])
        if FT not in data['forward'].keys():
            data['forward'][FT]={'lgE':[],'Xmax':[],'Xmumax':[]}
        to_update=data['forward'][FT]
        
    else:
        words=fname.split('_')
        Ms=float(words[1])
        Mc=int(words[2])
        try:
            Fr=int(words[3])
        except ValueError:#no fraction recorded (e.g. no final state)
            Fr=100
        if Fr not in data.keys():
            data[Fr]={}
        if Ms not in data[Fr].keys():
            data[Fr][Ms]={}
        if not Mc in data[Fr][Ms].keys():
            data[Fr][Ms][Mc]={'lgE':[],'Xmax':[],'Xmumax':[]}
            
        to_update=data[Fr][Ms][Mc]
    try:
        dd=root2array(data_dir+'/'+fname,'Shower')
        to_update['lgE']+=list(dd['lgE'])
        to_update['Xmax']+=list(dd['Xmax'])
        to_update['Xmumax']+=get_mu_max(dd)
    except IOError:
        print 'Error reading %s no Shower data' %fname
        errors+=1
print 'total files: %d' %no_files
print 'total errors: %d. %.2f percent of files' %(errors, 100.*float(errors)/float(no_files))
pdump(data,outname)
