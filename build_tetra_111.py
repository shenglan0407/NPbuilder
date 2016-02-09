#! /usr/bin/env python

##############################################################################
# Copyright 2016 Stanford University and the Author
#
# Author: Shenglan Qiao
#
# Makes Au tetrahedrons from ffc unit cells with 111 plane being the surfaces of
# the tetrahedron
# 
# 
#############################################################################


##############################################################################
# Imports
##############################################################################

import numpy as np
import os

import sys
import getopt

##############################################################################
# Code
##############################################################################
def usage():
    print './build_tetra_111.py -b <base_size> -o <output_file>\n'
    print '-b side of the base of the octahedron in angstroom\n'
    print '-o name of the file containing output coordinates\n'

def main(argv):
    # default values for options
    baseSize = 80.0 # 80 angstrom
    outputfile = 'test.xyz'
    
    a = 4.076 # unit cell length
    r = np.sqrt(2.0)*a/4.0 # radius of atoms as computed from unit cell length

    try:
        opts, args = getopt.getopt(argv,"hb:o:",["base_size=","output_file="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'help'
            usage()
            sys.exit()
        
        elif opt in ("-b", "--base_size"):
            baseSize = float(arg)
        
        elif opt in ("-o", "--output_file"):
            outputfile = arg
    
    x_max = y_max = int(baseSize/r)
    max_layer = x_max
    while os.path.isfile(os.getcwd()+'/'+outputfile):
        print "will not overwrite previous results. Please enter new output file name:"
        outputfile = raw_input()
    print "Adjusting size to %.3f to have integer number of atoms"%(x_max*r)
    print "Saving results to %s."%outputfile
        
    # this list will contain coordinates of all atoms in octahedron
    
    atoms=[]

    max_layer = x_max
    origin = np.array([0.,0.,0.])
    corner = np.array([0.,0.,0.])
    plane_growth_vector = np.array([1,0.,0.])
    layer_growth_vector = np.array([0,-2.*r/np.sqrt(3.),np.sqrt(6)*2.0/3.0*r])
    n_layer = 0
    while n_layer<max_layer:
        origin = corner
    
        for xx in range(x_max):
            atoms.extend([origin+2.0*r*k*plane_growth_vector for k in range(xx+1)])
    
            origin=origin+[-r,-np.sqrt(3.)*r,0.0]
        x_max-=1
        n_layer +=1
    
        corner = corner+layer_growth_vector

    with open(os.getcwd()+'/'+outputfile,'w') as output:
        output.write("%d\n"%len(atoms))
        output.write("building a pyramid\n")
        for this_atom in atoms:
            output.write("Au %.3f %.3f %.3f\n"%(this_atom[0],this_atom[1],this_atom[2]))


if __name__ == "__main__":
   main(sys.argv[1:])
    