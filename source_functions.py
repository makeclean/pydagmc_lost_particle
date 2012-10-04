# python module containing source functions of varying behaviours
import random
import math

pi = 3.14159265358979323846

def isotropic():

    theta = random.uniform(0,2*pi) 
    phi   = random.uniform(0,pi)

    u = math.cos(theta)*math.sin(phi)
    v = math.sin(theta)*math.sin(phi)
    w = math.cos(phi)

    uvw = (u,v,w)

    return uvw


def cone_z(angle):

    angle_pi=(float(angle)/180)*pi

    theta = random.uniform(0,angle_pi) 
    phi   = random.uniform(0,pi)

    u = math.cos(theta)*math.sin(phi)
    v = math.sin(theta)*math.sin(phi)
    w = math.cos(phi)

    uvw = (u,v,w)

    return uvw


def mono_dir(u,v,w):

    uvw=(u,v,w)

    return uvw
