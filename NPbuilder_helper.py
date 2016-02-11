from numpy import *
from itertools import groupby

def remove_overlapping(coors):
    """
    find and remove overlapping atoms from a list 
    of atomic coordinates (coors)

    coors should be a numpy array!   @ - @
    """
    c_strings= [ map(lambda xi: '%.3f'%xi, x ) 
                    for x in coors ]

    c_windex = [ [c[0],c[1],c[2],i] for i,c in enumerate(c_strings) ]

    key = lambda x: x[:3]
    c_windex_sort = sorted( c_windex, key=key)
    c_grouped = groupby( c_windex_sort, key=key)
    inds_to_keep = [ list(g[1])[0][3] for g in c_grouped ]

    num_overlap = len(coors) - len( inds_to_keep)

    print "Removing %d overlapping coordinates!"%num_overlap
    return array( coors)[inds_to_keep]

def mirrorZ_rotateZ(coors):
    """
    coors is a list of [[x,y,z], ... ]
    """
#   mirror translate
    atoms_mir = array( [ a for a in coors if a[2] > 0]  ) 
    atoms_mir[:,2] *=-1

#   rotate by 180
    rotZ = array( [ [-1., 0, 0],
                     [0, -1., 0],
                     [0, 0, 1.]] )
    atoms_mir = dot( rotZ, atoms_mir.T).T
    return atoms_mir


#dermen
