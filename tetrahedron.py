##############################################################################
# Copyright 2016 Stanford University and the Author
#
# Author: Shenglan Qiao
#
# Makes Au tetrahedrons from fcc unit cells with 111 plane being the surfaces of
# the tetrahedron
#############################################################################

import numpy as np
import os

def make_tetrahedron(u, v, origin, length, outfilename=None,
                    a=4.076, atomname='Au'):

    #while os.path.exists(outfilename):
    #    ask_for_file= "will not overwrite previous results.\
    #                    \nEnter new output file name: "
    #    outfilename = raw_input(ask_for_file)
    
#   spacing between 111 planes
    d111 = a/np.sqrt(3) 
    stack_vec = np.array([ 0, 0, d111])
    
#   distance between atoms from unit cell length
    r = a/np.sqrt(2)

    print "Saving results to %s."%outfilename
    
#   vector voodoo magic!    
    B = v-u 
    W = (u+v)
    W *= r/np.sqrt(3) / np.linalg.norm(W)
    stack_vec = np.cross( u,v)
    stack_vec *= d111 / np.linalg.norm(stack_vec)
    L = W + stack_vec

    atoms=[]
    for i_plane in xrange(length):
        for i_line in xrange(length-i_plane):
#           vector voodoo magica!
            line_origin = origin + i_plane*L + i_line*(r*u)
            line_vector = r*B
            atom_line = [line_origin + i_atom*line_vector
                                for i_atom in xrange(i_line+1)]
            atoms.extend( atom_line )
        
#   convert to string output and save
    if outfilename is not None:
        atoms_txt = [ '%s '%atomname + ' '.join(map(str,a)) 
                    for a in atoms]
        np.savetxt(outfilename, atoms_txt, fmt='%s')
    
    return atoms

if __name__ == "__main__":
    origin = np.zeros(3)
    length=25
    fname = 'tetra1_.xyz'
    u = np.array( [-.5, np.sqrt(3)/2., 0] )       
    v = np.array( [-1.,0,0 ])

    build_tetrahedron(u, v, origin, length, outfilename=fname) 
    



