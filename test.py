'''
Created on 29 Mar 2017

@author: kiera
'''

from root_numpy import root2array
import pylab as p

colours={'normal':'r','modified':'g'}
styles=colours.keys()

for style in styles:
    data=root2array('%s.root' %style,'Shower')
    for i in range(len(data['X'])):
        p.plot(data['X'][i],data['dEdX'][i],color=colours[style])
    p.plot([],[],color=colours[style],label=style)
    
p.legend()
p.show()