from numpy import *
from itertools import cycle
# makes pyramid with tip at 0,0,0
# and with the base as the x-y plane

def make_pyramid( u, v, outfilename, length=6, 
                    a=4.076, atomname='Au'):
    """
    Builds a square-base pyramid with top 
    vertex at 0,0,0
    
    'u,v' are unit vectors defining the base of the pyramid
    'outfilename' name of output txt file
    'length' is the number of atoms along a base edge
    'a' is the FCC lattice constant

    saves coordinates in .xyz format
    """
    planar_spacing = a/2.
#   size of the thing
    ndim = 2*length -1
    
    norm_uv = cross( u,v)
    norm_uv /= linalg.norm(norm_uv)


    layerA = zeros( (ndim, ndim) )
    layerB = zeros_like(layerA)
    layerA[::2, ::2] = 1
    layerB[1::2, 1::2] = 1
#e.g. if length==3:
#
#                  layerA
#    array([[ 1.,  0.,  1.,  0.,  1.],
#           [ 0.,  0.,  0.,  0.,  0.],
#           [ 1.,  0.,  1.,  0.,  1.],
#           [ 0.,  0.,  0.,  0.,  0.],
#           [ 1.,  0.,  1.,  0.,  1.]])
#
#                 layerB
#    array([[ 0.,  0.,  0.,  0.,  0.],
#           [ 0.,  1.,  0.,  1.,  0.],
#           [ 0.,  0.,  0.,  0.,  0.],
#           [ 0.,  1.,  0.,  1.,  0.],
#           [ 0.,  0.,  0.,  0.,  0.]])

    layerA = layerA.astype(bool)
    layerB = layerB.astype(bool)

#   make coordinates of {100} planes when looking down the 
#   {100} axis , i.e. at the  base
    coor = [ i* (.5*a/sqrt(2.)) for i in xrange(ndim) ]
    xyzmap = array( [  [coor[i], coor[j], 0] 
            for i in xrange(ndim) for j in xrange(ndim)] )
    xyzmap = xyzmap.reshape( (ndim, ndim, 3))

#   center the base at x,y = 0,0
    center = coor[ndim/2]
    xyzmap[:,:,0] -= center 
    xyzmap[:,:,1] -= center 

#   remap xyz such that it is oriented according to u,v plane
    X = xyzmap[:,:,0]
    Y = xyzmap[:,:,1]
    xyzremap = zeros_like( xyzmap)
    xyzremap[:,:,0] = u[0]*X + v[0]*Y
    xyzremap[:,:,1] = u[1]*X + v[1]*Y
    xyzremap[:,:,2] = u[2]*X + v[2]*Y #norm_uv[0]*X + norm_uv[1]*Y

#   check if the peak is in layerA or layerB 
#   (in above example peak is in layerA)
    if layerA[ndim/2,ndim/2]:
#       infinite generator
        layer_order = cycle( [layerA, layerB] )
    else:
        layer_order = cycle( [layerB, layerA] )
        
    atoms = []
    for i_plane in xrange(length):
        # array slice index
        ii = 2*i_plane
        x1,x2 =  (ndim-ii)/2, (ndim+ii)/2 +1 
        
        # select the layer
        layer = layer_order.next()
        
        # which points are on the lattice
        on_lattice = layer[ x1:x2, x1:x2]
        xyz = xyzremap[ x1:x2, x1:x2][on_lattice]
        
        # incremembt along normal vector to u,v
        stack_vec = planar_spacing * i_plane * norm_uv
        atoms.extend( xyz+stack_vec)

#   convert to string output and save
    atoms_txt = [ '%s '%atomname + ' '.join(map(str,a)) 
                for a in atoms]
    savetxt(outfilename, atoms_txt, fmt='%s')

if __name__ == "__main__":
    u = [ .5, -.5*sqrt(3), 0 ]
    v = [ .5, .5/sqrt(3), sqrt(6)/3. ] 
    fname = 'atoms_1.xyz'
    make_pyramid(u,v, fname)
