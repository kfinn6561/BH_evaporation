'''
Created on 2 Jul 2017

@author: kiera
'''
import pylab as p
import numpy as np
from plot_functions import *
from general_tools import pload
import sys

no_cl=True

try:
    fname=sys.argv[1]
except IndexError:
    fname='xmax_data.pkl'

data=pload(fname)

plot_folder='../plots/'

if 'no_cl' in data.keys():
    data.pop('no_cl')
    
if no_cl:
    no_cl_data=pload('non_classicalized_data.pkl') 
else:
    no_cl_data=[]

if not 'forward' in data.keys():
    print 'ERROR: No forward data in data file'
    sys.exit(1)
    
thresholds=data['forward'].keys()

for threshold in thresholds:
    