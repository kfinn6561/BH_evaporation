'''
Created on 3 Apr 2017

@author: kieran
'''
import pylab as p
import numpy as np
from functions import integrate

No_steps=100#number of numerical integration Steps
outfile='overlap_data.dat'

bs=np.linspace(0,2,1001)

def ct(y,b):
    return (b/np.sqrt(1-y**2))-1.

def integrand(b):
    return lambda y: np.nan_to_num((1-y**2)*(np.arccos(ct(y,b))-np.sqrt(1-ct(y,b)**2)*ct(y,b)))

def y_limit(b):
    return np.sqrt(1.-(b**2)/4.)

def overlap(b):
    return integrate(integrand(b),0.,y_limit(b),N=No_steps)

out=[]

for b in bs:
    out.append(overlap(b))
out=np.array(out)
out/=overlap(0.)    

f=open(outfile,'w')
for i in range(len(bs)-1):
    f.write('%f\n' %out[i])
f.write('%f'%out[-1])
f.close()

p.plot(bs,out)
p.xlabel('Impact Parameter')
p.ylabel('Relative overlap')
p.show()


