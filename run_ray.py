#!/usr/bin/python

# in order to use, the volume beyond the region you are testing, must be set to have a name of graveyard.

#import dagmc
from pydagmc import dagmc

# import time
import time

#import random number generator
import random

# import math library
import math

# import source functions
import source_functions

# import lost particle checker
import andy_geom_functions

#load geometry file

dagmc.load('watertight_out.h5m')
#dagmc.load('divertor_merged.h5m')

# find out where pos is
pos=(625.0,-43.4,0.0)
dir=(1.0,0.0,0.0)
first_vol=dagmc.find_volume(pos,dir)

# open output file for ray story
file = open("output.txt","a")

num_lost=0
nps = 10000000

for i in range(1,nps):

    if i%(nps/10)==0:
          localtime = time.asctime(time.localtime(time.time()))
          print (float(i)/float(nps))*100.0,'% complete', localtime
          print 'lost particle fraction = ',(float(num_lost)/float(nps))*100.0,'%'

 #  call an isotropic source
    uvw = source_functions.isotropic()

    volumes=list()
    positions=list()

    # set the iterator to produce xyz hit locations
    kw={"yield_xyz":'yield_xyz'}

    # intialise the ray iterator with appropriate values
    dagmc.ray_iterator(first_vol,pos,uvw,**kw)

    # loop through the ray history
    for (vol,dist,sur,xyz) in dagmc.ray_iterator(first_vol,pos,uvw,**kw):
         volumes.append(vol)
         positions.append(str(xyz))
  #       uvw = source_functions.isotropic()

  #       print xyz

    lost = andy_geom_functions.lost_particle(volumes)
    if lost == 0:
         num_lost +=1
# call dump2vtk, which takes the current ray history and prints it in nice format
         andy_geom_functions.dump_2_vtk(pos,positions,num_lost)

print 'done'

