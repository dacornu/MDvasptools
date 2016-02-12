# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 12:03:09 2016

@author: dcornu
"""
import numpy as np
import plotly
import plotly.graph_objs as go
import re

with open("XDATCAR", "r") as vaspfile: 
    vasp = vaspfile.readlines()

#Fractional to Cartesian coordinates
results = []
for v in vasp:
    results.append(v.split())	
parameter = float(vasp[1])
d=[]
for k in range(2,5):
    d.append(np.fromstring(vasp[k], sep=' '))

pos = []
n = 0
for k in range(7,len(vasp)):
    if re.match('Direct configuration', vasp[k]):
        n += 1
        pos.append('Direct configuration')
        pos.append('   ')
        pos.append(str(n))
    else:
        for i in range(3):
            kij = 0
            for j in range(3):
                kij += float(results[k][j])*parameter*float(d[j][i])
            pos.append(kij)

#Write the result 
xyz = open("XDATCARcart","w+")

for k in range(7):
    xyz.write(vasp[k])

for k in range(0,3*(len(vasp)-7),3):
    xyz.write( "{0} {1} {2}\n".format(pos[k], pos[k+1], pos[k+2] ) )
    
xyz.close()

#Create the array 'vasp' with all the lines of CONTCAR file
with open("XDATCARcart", "r") as vaspfile: 
    vasp = vaspfile.readlines()

# Number of Pt, C and O atoms
nPt = int(vasp[6].split()[0]) + int(vasp[6].split()[1])
nC = int(vasp[6].split()[2])
nO = int(vasp[6].split()[3])

#Vectors
d=[]
for k in range(2,5):
    d.append(np.fromstring(vasp[k], sep=' '))

# Erase Pt and O
n = 0
for v in vasp:
    n += 1
    if re.match('Direct configuration', v):
        vasp[n-1] = 'Erase'
        for k in range(nPt):
            vasp[n+k] = 'Erase'
        for k in range(nO):
            vasp[n+nPt+nC+k] = 'Erase'

# Erase first lines
for i in range(7):
    vasp[i] = 'Erase'

#Write the result in the .xyz file
#1 Write the number of atoms and the comment
xyz = open("XDATCAR-temp","w+")
for v in vasp:
    if v != 'Erase':
        xyz.write(v)
xyz.close()

with open("XDATCAR-temp", "r") as vaspfile: 
    vasp = vaspfile.readlines()

#Datapoints
v=[]
for k in range(len(vasp)):
    v.append(np.fromstring(vasp[k], sep=' '))

#Creation of boxes
Nx = int(raw_input('Number of boxes (x direction): '))
Ny = int(raw_input('Number of boxes (y direction): '))

map = []
for i in range(Ny):
    map.append([0]*Nx)

#Limits of boxes
cx = (d[0][0]+d[1][0])/Nx
cy = d[1][1]/Ny

for k in v:
    x = k[0]
    y = k[1]
    for n1 in range(Nx):
        if n1*cx <= x and (n1+1)*cx > x:
            for n2 in range(Ny):
                if n2*cy <= y and (n2+1)*cy > y:
                    map[n2][n1] += 1

data = [
    go.Heatmap(
        z=map,
    )
]
plot_url = plotly.offline.plot(data, filename='heatmap.html')