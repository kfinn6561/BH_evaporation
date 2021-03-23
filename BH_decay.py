'''
Created on 14 Nov 2016

@author: kieran
'''

import pylab as p
import numpy as np
from plottools import get3dax
from copy import copy
from scipy.special import lambertw
from general_tools import progress_bar

m=0.5#mass of the emitted particle
Mp=1000.#planck mass, GeV
N0=0.01#Nscaling
N0=1.

def mat_x_vec(mat,vec):
    return np.array(mat*np.matrix(vec).T).T[0]
'''
def calc_N(M):
    return (M/Mp)**2
def calc_M(compare_numbers):#these have the right scalings. Need to put in numerical factors if precision becomes important
    return np.sqrt(float(compare_numbers))*Mp
'''

def calc_N(M):
    return N0*(M/m)*lambertw(M*m/(Mp**2)).real
def calc_M(N):
    return m*(N/N0)/lambertw(np.sqrt(N/N0)*m/(2*Mp)).real

#M1=calc_M(1)


def calc_mass(p):#get mass from four-momentum
    m2=p[0]**2-p[1]**2-p[2]**2-p[3]**2
    return np.sqrt(m2)

def calc_lorentz(p):
    m0=calc_mass(p)
    gamma=p[0]/m0
    bg=np.sqrt(gamma**2-1.)#beta*gamma
    pp=np.sqrt(p[1]**2+p[2]**2+p[3]**2)
    if pp>0:
        nx=-p[1]/pp
        ny=-p[2]/pp
        nz=-p[3]/pp
    else:
        nx=ny=nz=0
    out=[[gamma,-bg*nx,-bg*ny,-bg*nz],
         [-bg*nx,1.+(gamma-1)*nx**2,(gamma-1)*nx*ny,(gamma-1)*nx*nz],
         [-bg*ny,(gamma-1)*ny*nx,1.+(gamma-1)*ny**2,(gamma-1)*ny*nz],
         [-bg*nz,(gamma-1)*nz*nx,(gamma-1)*nz*ny,1.+(gamma-1)*nz**2]]
    return np.matrix(out)
    
    
def spit_particle(p0,N):
    cos_theta=np.random.uniform(-1,1)
    sin_theta=np.sqrt(1-cos_theta**2)*np.random.choice([1,-1])
    phi=np.random.uniform(0,2*np.pi)
    M0=calc_mass(p0)
    
    if N==2:
        E1=M0/2.
    else:
        E1=(1./2.)*((M0**2+m**2-calc_M(N-1)**2)/M0)
    p1=np.sqrt(E1**2+m**2)
    
    p_cm=np.array([0,sin_theta*np.cos(phi),sin_theta*np.sin(phi),cos_theta])*p1+E1*np.array([1.,0,0,0])
    
    L=calc_lorentz(p0)
    p1=mat_x_vec(L,p_cm)
    
    #p2_cm=np.array([1.,0,0,0])*M0-p_cm
    #p2=mat_x_vec(L,p2_cm)
    
    p2=p0-p1
    return [p2,p1]
    

def get_distribution(N):
    P0=np.array([1.,0.,0.,0.])*calc_M(N)#4-momentum of the initial BH
    return calc_decay(P0,N)
    
def calc_decay(P0,N=False):
    if not N:
        N=int(calc_N(calc_mass(P0)))
    if N<=1:
        return ([P0],[P0])
    out=[]
    condensate_states=[P0]
    N0=copy(N)
    while N>2:
        progress_bar(N0-N,N0)
        P0,p1=spit_particle(P0,N)
        out.append(p1)
        condensate_states.append(copy(P0))
        N-=1
    out+=spit_particle(P0, N)#final two
    return (out, condensate_states)
    
def get_energies(Ps):
    out=[]
    for pp in Ps:
        out.append(pp[0])
    return np.array(out)

def get_rapidity(Ps):
    out=[]
    for pp in Ps:
        out.append(np.arcsinh(pp[1]/m))
    return np.array(out)

def get_particle_rapidity(Ps):
    out=[]
    for pp in Ps:
        out.append(0.5*np.log((pp[0]+pp[1])/(pp[0]-pp[1])))
    return np.array(out)

def get_pt(Ps):
    out=[]
    for pp in Ps:
        out.append(np.sqrt(pp[2]**2+pp[3]**2))
    return out
    
def plot_final_state(Ps):
    ax=get3dax()
    for pp in Ps:
        ax.plot([0,pp[1]],[0,pp[2]],[0,pp[3]])
    return ax

def arrow_final_state(Ps):
    ax=get3dax()
    zero=np.zeros(len(Ps))
    X=[]
    Y=[]
    Z=[]
    for pp in Ps:
        ax.plot([0,pp[1]],[0,pp[2]],[0,pp[3]])
        X.append(pp[1])
        Y.append(pp[2])
        Z.append(pp[3])
    ax.quiver(zero,zero,zero,X,Y,Z,pivot='tail')
    ax.set_xlim(-2,2)
    ax.set_ylim(-2,2)
    ax.set_zlim(-2,2)
    return ax

def zoom(ax,l):
    ax.set_xlim(-l,l)
    ax.set_ylim(-l,l)
    ax.set_zlim(-l,l)
    
def boost_x(gamma,X):
    beta=np.sqrt(1-1./(gamma**2))
    Lambda=np.matrix([[gamma,-beta*gamma,0,0],
                      [-beta*gamma,gamma,0,0],
                      [0,0,1.,0],
                      [0,0,0,1.]])
    out=[mat_x_vec(Lambda, x) for x in X]
    return out

def plot_random_walk(X):
    ax=get3dax()
    x=[]
    y=[]
    z=[]
    for pp in X:
        x.append(pp[1])
        y.append(pp[2])
        z.append(pp[3])
    ax.plot(x,y,z)
    ax.plot([0],[0],[0],'go')
    ax.plot([x[-1]],[y[-1]],[z[-1]],'ro')
    return ax
    
        
if __name__=="__main__":
    '''
    compare_numbers=1000
    gamma=100.
    P_com,P_con=get_distribution(compare_numbers)
    P_lab=boost_x(gamma,P_com)
    
    ax_rw=plot_random_walk(P_con)
    zoom(ax_rw,0.5)
    
    ax_fs=plot_final_state(P_com)
    zoom(ax_fs,0.1)
    
    p.figure()
    p.hist(get_energies(P_com),1000)
    p.title('rapidity distribution')
    
    p.figure()
    p.hist(np.log(get_energies(P_com)),100)
    p.title('log rapidity distribution')
    
    pt=[np.sqrt(x[2]**2+x[3]**2) for x in P_com]
    p.figure()
    p.hist(pt,1000)
    p.title('Pt distribution')
    '''
    
    E=1e20/1e9#10^20eV in GeV
    m0=0.94#proton mass
    gamma=E/m0
    M_com=np.sqrt(2*E*m0)#com energy in collision with proton
    N=int(calc_N(M_com))
    print N
    print gamma
    print M_com
    
    P_com,P_con=get_distribution(N)
    P_lab=boost_x(gamma,P_com)
    
    rhos=get_particle_rapidity(P_lab)
    rho_com=get_particle_rapidity(P_com)
    
    
    p.figure()
    p.hist(rhos,100)
    p.title('rapidity distribution')
    
    '''
    p.figure()
    p.hist(np.log(rhos),100)
    p.title('log rapidity distribution')
    '''
    
    p.figure()
    p.hist(rho_com,100)
    p.title('com rapidity distribution')
    
    
    p.show()
    
    