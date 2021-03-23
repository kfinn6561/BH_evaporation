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

def E2bod(m0,m1,m2):
    return (1./(2*m0))*(m0**2+m1**2-m2**2)

def p2bod(m0,m1,m2):
    return np.sqrt(E2bod(m0,m1,m2)**2-m1**2)

def X_max(E):
    return X0*np.log(E/Ec)

def N_max(E):
    return (0.31/np.sqrt(np.log(E/Ec)-0.33))*(E/Ec)

def GH_func(E,X1):
    N=N_max(E)
    xm=X_max(E)+X1
    return lambda x: np.nan_to_num(N*np.power((x-X1)/(xm-X1),(xm-X1)/lambda_N)* np.exp((xm-x)/lambda_N))

def GH_fit(x,N,X1,xm,l):
    return np.nan_to_num(N*np.power((x-X1)/(xm-X1),(xm-X1)/l)* np.exp((xm-x)/l))

def double_GH_fit(x,N_1,X1_1,xm_1,l_1,N_2,X1_2,xm_2,l_2):
    return np.nan_to_num(N_1*np.power((x-X1_1)/(xm_1-X1_1),(xm_1-X1_1)/l_1)* np.exp((xm_1-x)/l_1))+np.nan_to_num(N_2*np.power((x-X1_2)/(xm_2-X1_2),(xm_2-X1_2)/l_2)* np.exp((xm_2-x)/l_2))


def nice_name(E):
    if E>=1e9:
        return '%dEeV' %(E/1e9)
    elif E>=1e6:
        return '%dPeV' %(E/1e6)
    elif E>=1e3:
        return '%dTeV' %(E/1e3)
    elif E<1:
        return '%dMeV' %(E*1e3)
    else:
        return '%dGeV' %E

def double_bang_profile(E0,y,X2):
    E1=E0*(1-y)
    E2=(E0-E1)#todo, add more sophisticated energy split
    f1=GH_func(E1, 0)
    f2=GH_func(E2, X2)
    f3=lambda x:f1(x)+f2(x)
    return (f1,f2,f3)

def plot_double_bang(xx,fs):
    f1,f2,f3=fs
    y1=f1(xx)
    y2=f2(xx)
    y3=f3(xx)
    p.plot(xx,y1,color='r')
    p.plot(xx,y2,color='b')
    p.plot(xx,y3,color='k')



class particle():
    def __init__(self,name,mass,lifetime):
        self.name=name
        self.mass=mass
        self.lifetime=lifetime
        
proton=particle('proton',0.938,0.)       
       
def double_bang(E0,daughter,secondary=proton):
    x1=gluon_pdf(np.random.random())
    x2=gluon_pdf(np.random.random())
    x_ave=np.sqrt(x1*x2)
    m0=x_ave*np.sqrt(2*E0*proton.mass)#assumes collision was with non-relativistic proton. m0 is COM energy
    m1=daughter.mass
    m2=secondary.mass
    if m0<(m1+m2):#production is not possible
        f1=GH_func(E0, 0.)
        f2=lambda x:np.zeros_like(x)
        return [f1,f2,f1]
    
    E=E2bod(m0, m1, m2)
    p=p2bod(m0, m1, m2)
    ymin=x_ave*(E-p)/m0
    ymax=x_ave*(E+p)/m0
    
    y=(ymax-ymin)*np.random.random()+ymin
    gamma=y*E0/m1
    t=np.random.exponential(gamma*daughter.lifetime)#decay time
    l=c*t*rho#distance travelled in g/cm^2
    return double_bang_profile(E0, y, l)

def sample(f,ct=0.42,N=100):
    xmax=840./ct#maximum column depthe before hitting earth
    x=np.sort(np.random.random(N)*xmax)#sample the profile at N random locations (this may need to change)
    y0=f(x)#centre of distribution
    '''try:
        y1=np.random.poisson(y0).astype(float)#add poisson noise
    except ValueError:
        y1=y0#if y0 is too large, cannot add poisson noise, but should be subdominant anyway'''
    y2=np.random.normal(y0,0.1*y0+1e-5)#add 10/% detector noise 1e-5 prevents errors when y1=0
    return (x,y2)


def find_fit(x,y,verbose=False):
    i=np.argmax(y)
    x1=0.
    xm=x[i]
    n=y[i]
    l=lambda_N#this will have to change if normalisation applied
    return curve_fit(GH_fit,x,y,p0=[n,x1,xm,l],sigma=0.1*y+1.)


def prob_detect_func(f,N=100):
    out=[]
    for i in range(N):
        x,y=sample(f,ct=np.random.random())
        temp=find_fit(x,y)
        if temp!='fail':
            temp=zero_dist.cdf(temp)
            out.append(temp)
    return (np.mean(out),np.std(out))

def prob_detect_part(E0,part,N=1000):
    out=[]
    for i in range(N):
        _,_,f=double_bang(E0, part)
        x,y=sample(f,ct=np.random.random())
        temp=find_fit(x,y)
        if temp!='fail':
            temp=zero_dist.cdf(temp)
            out.append(temp)
    return out

