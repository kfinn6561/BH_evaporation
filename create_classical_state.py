'''
Created on 17 Feb 2017

@author: kieran
'''
import numpy as np
from copy import copy

m=0.#mass of the emitted particle
Mp=1.#planck mass, use planck units

def mat_x_vec(mat,vec):
    return np.array(mat*np.matrix(vec).T).T[0]

def calc_N(M):
    return (M/Mp)**2
def calc_M(N):#these have the right scalings. Need to put in numerical factors if precision becomes important
    return np.sqrt(float(N))*Mp

M1=calc_M(1)


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
    
    
def spit_particle(p0,final=False):
    cos_theta=np.random.uniform(-1,1)
    sin_theta=np.sqrt(1-cos_theta**2)*np.random.choice([1,-1])
    phi=np.random.uniform(0,2*np.pi)
    M0=calc_mass(p0)
    
    if final:
        E1=M0/2.
    else:
        E1=(1./2.)*((M1**2+m**2)/M0)
    p1=np.sqrt(E1**2+m**2)
    
    p_cm=np.array([0,sin_theta*np.cos(phi),sin_theta*np.sin(phi),cos_theta])*p1+E1*np.array([1.,0,0,0])
    
    L=calc_lorentz(p0)
    p1=mat_x_vec(L,p_cm)
    
    #p2_cm=np.array([1.,0,0,0])*M0-p_cm
    #p2=mat_x_vec(L,p2_cm)
    
    p2=p0-p1
    return [p2,p1]
    

def get_distribution(N):
    out=[]
    P0=np.array([1.,0.,0.,0.])*calc_M(N)#4-momentum of the initial BH
    condensate_states=[P0]
    while N>2:
        P0,p1=spit_particle(P0)
        out.append(p1)
        condensate_states.append(copy(P0))
        N-=1
    out+=spit_particle(P0, final=True)#final two
    return (out, condensate_states)
    
def get_energies(Ps):
    out=[]
    for pp in Ps:
        out.append(pp[0])
    return out

def get_pt(Ps):
    out=[]
    for pp in Ps:
        out.append(np.sqrt(pp[2]**2+pp[3]**2))
    return out

    
def boost_x(gamma,X):
    beta=np.sqrt(1-1./(gamma**2))
    Lambda=np.matrix([[gamma,-beta*gamma,0,0],
                      [-beta*gamma,gamma,0,0],
                      [0,0,1.,0],
                      [0,0,0,1.]])
    out=[mat_x_vec(Lambda, x) for x in X]
    return out