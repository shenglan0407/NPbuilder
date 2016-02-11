from numpy import *

from tetrahedron import make_tetrahedron
from pyramid import make_pyramid

from NPbuilder_helper import remove_overlapping, mirrorZ_rotateZ

atoms= []

origin = zeros(3)
length=10

# 1st tetrahedron 1
u = array( [-.5, sqrt(3)/2., 0] ) 
v = array( [-1.,0,0 ])
atoms.extend( make_tetrahedron(u, v, origin, length) )

#2nd tetrahedron 2
u = array( [-.5, -sqrt(3)/2., 0] )       
v = array( [.5,-sqrt(3)/2.,0 ])
atoms.extend( make_tetrahedron(u, v, origin, length) )

#3rd for tetrahedron 3
u = array( [1,0,0 ])
v = array( [.5, sqrt(3)/2., 0] )       
atoms.extend( make_tetrahedron(u, v, origin, length) )

# 4th tetrahedron (the one on the top)
u = array( [.5, .5/sqrt(3),sqrt(6)/3.] ) 
v = array( [ -.5, .5/sqrt(3), sqrt(6)/3. ] )
atoms.extend( make_tetrahedron(u, v, origin, length) )

# 1st pyramid
u = [ .5, -.5*sqrt(3), 0 ]
v = [ .5, .5/sqrt(3), sqrt(6)/3. ] 
atoms.extend( make_pyramid(u, v, length) )

# 2nd pyramid
u = [ -1, 0,0 ] 
v = [ 0, -1/sqrt(3), sqrt(6)/3. ] 
atoms.extend( make_pyramid(u, v, length) )

# 3rd pyramid
u = [ .5, .5*sqrt(3), 0 ]
v = [ -.5, .5/sqrt(3), sqrt(6)/3. ] 
atoms.extend( make_pyramid(u, v, length) )

# mirror and rotate!
atoms = vstack((atoms, 
                mirrorZ_rotateZ(atoms))
                )

# remove the overlapping coordinates!
atoms = remove_overlapping( atoms)

# save the beautiful cuboctahedron! 
#    awww its so cute  ^.^
atoms_txt = [ 'Au ' + ' '.join(map(str,a)) 
                    for a in atoms]
savetxt('cuboctahedron_10.xyz', atoms_txt, fmt='%s')

#dermen
