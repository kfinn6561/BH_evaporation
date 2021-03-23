import pylab as p
import numpy as np
from collections import defaultdict

xmumax_dname='../Data/PA_xmumax_data'

def read_in_PA_data(fname='../Data/PA_xmax_data/xmaxMoments.txt'):
    f=open(fname,'r')
    r=f.readlines()
    f.close()
    headers=['energyBin','lgMinEnergy','lgMaxEnergy','meanLgEnergy','numberOfEvents',
             'meanXmax','meanXmaxSigmaStat','meanXmaxSigmaSysUp','meanXmaxSigmaSysLow',
             'sigmaXmax','sigmaXmaxSigmaStat','sigmaXmaxSigmaSysUp','sigmaXmaxSigmaSysLow']
    out={header:[] for header in headers}
    for line in r:
        numbers=line.split()
        for i in range(len(headers)):
            out[headers[i]].append(float(numbers[i]))
    for header in headers:
        out[header]=np.array(out[header])
    return out

PA_data=read_in_PA_data()

def read_csv(fname):
    f=open(fname,'r')
    x=[]
    y=[]
    for line in f:
        words=line.split(',')
        x.append(float(words[0]))
        y.append(float(words[1]))
    f.close()
    return (x,y)

def plot_series(data,axes, colour='k',label='',NO_CL=False, xm='Xmax'):
    ax_mean,ax_sigma=axes
    Es=data['lgE']
    xmax=data[xm]
    data_dict=defaultdict(list)
    for i in range(len(Es)):
        data_dict[Es[i]].append(xmax[i])
    sorted_Es=np.sort(data_dict.keys())
    mean=[]
    sigma=[]
    for E in sorted_Es:
        mean.append(np.mean(data_dict[E]))
        sigma.append(np.std(data_dict[E]))
    if NO_CL:
        lw=6
        color='k'
        label='no cl'
    else:
        lw=3
        color=colour
    ax_mean.plot(sorted_Es,mean,color=color,lw=lw,label=label)
    ax_sigma.plot(sorted_Es,sigma,color=color,lw=lw)

def get_axes(no_cl_data=[], mu=False):
    if mu:
        xm='Xmumax'
    else:
        xm='Xmax'
    fig,axes=p.subplots(2,1,sharex=True,figsize=(18,12))
    ax_mean,ax_sigma=axes
    ax_sigma.set_xlabel('Log(E/eV)',fontsize=24)
    ax_mean.set_ylabel('Mean %s (g/cm^-2)' %xm,fontsize=24)
    ax_sigma.set_ylabel('RMS %s (g/cm^-2)'%xm,fontsize=24)
    
    if no_cl_data!=[]:
        plot_series(no_cl_data,axes,xm=xm,NO_CL=True)
        
    if mu:
        y,x=read_csv(xmumax_dname+'/x_mumax_mean.csv')
        ax_mean.plot(x,y,marker='o',color='k',ls='',ms=20,lw=6,label='PA data')
        
        y,x=read_csv(xmumax_dname+'/x_mumax_sigma.csv')
        ax_sigma.plot(x,y,marker='o',color='k',ls='',ms=20,lw=6,label='PA data')
    else:
        ax_mean.errorbar(PA_data['meanLgEnergy'],PA_data['meanXmax'],
                     yerr=[PA_data['meanXmaxSigmaSysUp']+PA_data['meanXmaxSigmaStat'],PA_data['meanXmaxSigmaStat']-PA_data['meanXmaxSigmaSysLow']],
                     fmt='o',color='k',ms=20,lw=6,label='PA data')
            
            
        ax_sigma.errorbar(PA_data['meanLgEnergy'],PA_data['sigmaXmax'],
                     yerr=[PA_data['sigmaXmaxSigmaSysUp']+PA_data['sigmaXmaxSigmaStat'],PA_data['sigmaXmaxSigmaStat']-PA_data['sigmaXmaxSigmaSysLow']],
                     fmt='o',color='k',ms=20,lw=6)
            
    #ax_sigma.legend(ncol=2,loc='upper right',columnspacing=0.2,handletextpad=0.1,borderpad=0.1)
    ax_sigma.set_ylim(20,85)
    if mu:
        ax_mean.set_ylim(450,650)
    else:
        ax_mean.set_ylim(670,900)
    
    ax_sigma.set_xlim(17.8,20)
    return (fig,axes)