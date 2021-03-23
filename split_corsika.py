'''
Created on 20 Oct 2016

@author: kieran
'''

def strip_comments(lines):
    out=[]
    for line in lines:
        if line[0]!='#':
            out.append(line)
    return out

infile='corsika_compiled.F'
subdir='subroutines'
header='SUBROUTINE'

infile='soubroutines/CORSIKAMAIN.F'
subdir='subroutines/entries'
header='ENTRY'

f=open(infile,'r')
lines=f.readlines()
f.close()

#lines=strip_comments(lines)

start_nos=[]
for i in range(len(lines)):
    if lines[i].strip()[:len(header)]==header:
        start_nos.append(i)

for i in range(len(start_nos)):
    start=start_nos[i]
    if i!=len(start_nos)-1:
        finish=start_nos[i+1]
    else:
        finish=len(lines)
    name=lines[start].strip()[len(header):].split('(')[0].strip()
    f=open('%s/%s.F'%(subdir,name),'w')
    print name
    for j in range(start,finish):
        f.write(lines[j])
    f.close()