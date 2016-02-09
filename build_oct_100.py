#! /usr/bin/env python

##############################################################################
# Copyright 2016 Stanford University and the Author
#
# Author: Shenglan Qiao
#
# Makes Au octahedrons from ffc unit cells
#
# Generates repeated coordinates at the moment!
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
    print './build_gold_oct.py -b <base_size> -o <output_file>\n'
    print '-b size of the square base of the octahedron in angstroom\n'
    print '-o name of the file containing output coordinates\n'
    print 'Currently generates repeated coordinates. Use with caution.'

def main(argv):
    # default values for options
    baseSize = 80.0 # 80 angstrom
    outputfile = 'test.xyz'
    
    a = 4.076 # unit cell length
    max_cell = int(baseSize/a)
    # make sure max_cell is odd so we get a pyramid
    if max_cell%2==0:
        max_cell+=1
    
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
            max_cell = int(baseSize/a)
            # make sure max_cell is odd so we get a pyramid
            if max_cell%2==0:
                max_cell+=1
        
        elif opt in ("-o", "--output_file"):
            outputfile = arg
            
    while os.path.isfile(os.getcwd()+'/'+outputfile):
        print "will not overwrite previous results. Please enter new output file name:"
        outputfile = raw_input()
    print "Adjusting size to %.3f to make perfect pyramid"%(max_cell*a)
    print "Saving results to %s."%outputfile
        
    # this list will contain coordinates of all atoms in octahedron
    atoms = []
    n_layer = 0
    n_cell = max_cell
    # the first layer has max_cell unit cells.
    while n_cell >0:
        # each layer has n_cell by n_cell
        for xx in range(n_cell):
            for yy in range(n_cell):
                # this is the origin of each unit cell
                # origin is moved as we grow the layer of the pyramid
                origin=[(xx+n_layer)*a,(yy+n_layer)*a,n_layer*a]
                
                origin=np.array(origin)
                atoms.append(origin)
                atoms.append(origin+[0.5*a,0.5*a,0.])
                if xx!=n_cell-1:
                    atoms.append(origin+[a,0.5*a,0.5*a])
                else:
                    atoms.append(origin+[a,a,0.])
                    atoms.append(origin+[a,0.,0.])
                if yy!=n_cell-1:
                    atoms.append(origin+[0.5*a,a,0.5*a])
                else:
                    atoms.append(origin+[0.,a,0.])
                    if xx!=n_cell-1:
                        atoms.append(origin+[a,0.,0.])
    
        n_layer+=1
        n_cell-=2

    # reflect to generate the second half of octahedron
    
    # reflection = []
#     for this_atom in atoms:
#         if this_atom[2]!=0:
#             reflection.append([this_atom[0],this_atom[1],-this_atom[2]])
#     atoms.extend(reflection)

    with open(os.getcwd()+'/'+outputfile,'w') as output:
        output.write("%d\n"%len(atoms))
        output.write("building a pyramid\n")
        for this_atom in atoms:
            output.write("Au %.3f %.3f %.3f\n"%(this_atom[0],this_atom[1],this_atom[2]))


if __name__ == "__main__":
   main(sys.argv[1:])
    