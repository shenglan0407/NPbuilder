import math
import sys
import os
from random import random

from math import sqrt

#a = 5.902
#c = 9.255

# from science paper
# http://www.sciencemag.org/content/316/5832/1726.abstract
a = 5.95
c = 9.06

pv1 = ( 0.5 * a , -0.5 * sqrt(3.) * a , 0.)
pv2 = ( 0.5 * a ,  0.5 * sqrt(3.) * a , 0.)
pv3 = (      0.,                   0., c )


sizex = sqrt(  pv1[0]**2 + pv2[0]**2 + pv3[0]**2 )
sizey = sqrt( pv1[1]**2 + pv2[1]**2 + pv3[1]**2 )
sizez = sqrt( pv1[2]**2 + pv2[2]**2 + pv3[2]**2 )


atoms = []
for i in open("./feh_unit_cell.coor","r").readlines():
	i = i.strip().split()
	x = i[0]
	y = i[1]
	z = i[2]
	F = i[3]
	atom_coors = ( float(x),float(y),float(z),float(F) )
	atoms.append ( atom_coors )

atoms = tuple ( atoms ) 

atom_per_unit   = len( atoms )

size_in_nm  = float ( input("size [diameter] in nm: " ) ) 

size_in_ang = size_in_nm * 10.

center      = ( size_in_ang / 2., size_in_ang / 2., size_in_ang / 2. )

out_file_name = 'feh_sphere_'+ str( size_in_nm) + 'nm.coor'
out_file = open( out_file_name,'w')


u1 = 0.
while u1 < size_in_ang:
    u2 = 0.
    while u2 < size_in_ang:
        u3 = 0.
        while u3 < size_in_ang:
            i = 0
            ux = u1*pv1[0]/sizex + u2*pv2[0]/sizex + u3*pv3[0]/sizex
            uy = u1*pv1[1]/sizey + u2*pv2[1]/sizey + u3*pv3[1]/sizey
            uz = u1*pv1[2]/sizez + u2*pv2[2]/sizez + u3*pv3[2]/sizez
            print u1/sizex
            print u2/sizey
            print u3/sizez
            while i < atom_per_unit:
                atomX = ux + atoms[i][0]
                atomY = uy + atoms[i][1]
                atomZ = uz + atoms[i][2]
                atomID= atoms[i][3]
                radius = sqrt( ( atomX - center[0] )**2 + \
                               ( atomY - center[1] )**2 + \
                               ( atomZ - center[2] )**2  ) 
                if radius <= size_in_ang / 2:
                    print >> out_file , atomX,atomY,atomZ,atomID
                i += 1
            u3 += sizez
        u2 += sizey
    u1 += sizex

out_file.close()

print "wrote file", 'feh_sphere_'+ str( size_in_nm) + 'nm.coor' ,"."

