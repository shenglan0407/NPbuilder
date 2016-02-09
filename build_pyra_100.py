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
    r = a/(2.0*np.sqrt(2.0)) # radius of atoms
    
    x_max = int(baseSize/a)+1
    
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
            x_max = int(baseSize/a)+1
        
        elif opt in ("-o", "--output_file"):
            outputfile = arg
            
    while os.path.isfile(os.getcwd()+'/'+outputfile):
        print "will not overwrite previous results. Please enter new output file name:"
        outputfile = raw_input()
    print "Adjusting size to %.3f to make perfect pyramid"%((x_max-1)*a)
    print "Saving results to %s."%outputfile
        
    # this list will contain coordinates of all atoms in octahedron
    atoms=[]


    max_layer = x_max
    
####################################################################################################
# 
# Change origin, corner, and growth vectors below
# 
####################################################################################################
    # change origin, plane_growth_vector1, plane_growth_vector2
    origin = np.array([0.,0.,0.])
    corner = origin
    plane_growth_vector1 = np.array([2.0*np.sqrt(2.0),0.,0.])*r
    plane_growth_vector2 = np.array([np.sqrt(2.0),np.sqrt(2.0),0.])*r
    
    #this vector should be (plane_growth_vector1+0.5*plane_growth_vector2)+[0,0,sqrt(2)]*r. Check this!
#     layer_growth_vector1 = np.array([2.0*np.sqrt(2.0),np.sqrt(2.0),np.sqrt(2.0)])*r
    layer_growth_vector1 = (plane_growth_vector1+plane_growth_vector2*2.0)*0.5+[0,0,np.sqrt(2)]*r
    
    #this vector should be [lane_gorwth_vector2*0.5+[0,0,sqrt(2)]*r. Check this!
#     layer_growth_vector2 = np.array([0.,np.sqrt(2.0),np.sqrt(2.0)])*r
    layer_growth_vector2 = plane_growth_vector2-0.5*plane_growth_vector1+[0,0,np.sqrt(2)]*r
    
####################################################################################################
# 
# end of growth vectors block
# 
####################################################################################################    
    
    n_layer = 0
    while n_layer<max_layer:
        y_max = x_max
        origin = corner
        total_rows = x_max*2-1
        for xx in range(total_rows):
            if n_layer%2==0:
                atoms.extend([origin+plane_growth_vector1*k for k in range(y_max)])
                if xx%2==0:
                    origin=origin+plane_growth_vector2
                    y_max-=1
                else:
                    origin=origin+plane_growth_vector2*np.array([-1,1,1])
                    y_max+=1
            else:
                atoms.extend([origin+plane_growth_vector1*k for k in range(y_max-1)])
                if xx%2==1:
                    origin=origin+plane_growth_vector2
                    y_max-=1
                else:
                    origin=origin+plane_growth_vector2*np.array([-1,1,1])
                    y_max+=1
                
        x_max-=1
        n_layer +=1
        if n_layer%2==1:
            corner = corner+layer_growth_vector1
        else:
            corner = corner+layer_growth_vector2
        

    with open(os.getcwd()+'/'+outputfile,'w') as output:
        output.write("%d\n"%len(atoms))
        output.write("building a pyramid\n")
        for this_atom in atoms:
            output.write("Au %.3f %.3f %.3f\n"%(this_atom[0],this_atom[1],this_atom[2]))


if __name__ == "__main__":
   main(sys.argv[1:])
    