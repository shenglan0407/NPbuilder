from pylab import *

from NPbuilder_helper import remove_overlapping

outfile_pre = 'decahedron_Feb2015'

#################
# SOME PARAMETERS
##################
a_gold = 4.079 
Z_gold = 79.
# pure fcc decahedron
th = arccos( sqrt( 2./3. ) )
# express FCC cell as equivalent orthrhombic cell
a = a_gold /  sqrt(2.)
b = sqrt(4.-(1/sin(th))**2) * a_gold / sqrt(2.)
c = (1./tan(th)) * a_gold / sqrt(2.)

n_layers = 20 # size of the tetra

######################
# MAKE THE TETRAHEDRAL TWIN
# 
coor_file = open(outfile_pre+'.coor','w')
# initial atom
print >> coor_file,  0.,0.,0.,Z_gold 

atoms = zeros( (1,3) )
shift = array( [ -a/2., b/2., c/2. ] )
for layer in xrange(1, n_layers):
    # shift old atoms in y-direction
    atoms += array([0,b,0]) 
    
    # make new layers of atoms
    new_atoms = vstack( [ [ i*a,0,0  ] 
                           for i in xrange( layer+1 ) ]  )
    new_atoms += layer*shift
    
#   combine 
    atoms = vstack( (atoms, new_atoms))

#   save
    for atom in atoms:
        print >> coor_file,\
                atom[0],\
                atom[1],\
                atom[2] ,\
                Z_gold
# save the coor file (tetrahedral unit)
coor_file.close()

def rot_y(angle):
    return array( [[cos(angle), 0., -sin(angle)] ,
                    [0.,1.,0. ],
                    [sin(angle),0.,cos(angle)]])

####################
# MAKE A DECAHEDRON
###################
# pure fcc
beta = 70.53 * pi / 180.

# load all the atoms we saved
xyz0 = loadtxt(outfile_pre+'.coor')[:,:3]
# apply rotations
xyz1 = dot( rot_y(beta), xyz0.T).T
xyz2 = dot( rot_y(beta), xyz1.T).T
xyz3 = dot( rot_y(beta), xyz2.T).T
xyz4 = dot( rot_y(beta), xyz3.T).T

xyz_all = vstack( ( xyz0, xyz1, xyz2 , xyz3, xyz4 ) ) 
xyz_all = remove_overlapping(xyz_all)



Z_all = ones( (xyz_all.shape[0], 1 ) )* Z_gold

# save x,y,z,atomZ in a .coor file (decahedron)
xyz_atomZ = hstack((xyz_all, Z_all) )
savetxt(outfile_pre+'2.coor', xyz_atomZ )

# save an xyz file for viewing in PyMol
xyz_file = open(outfile_pre+'.xyz', 'w')
for i in xrange(xyz_all.shape[0]):
    print>> xyz_file, "Au",\
            xyz_all[i,0],\
            xyz_all[i,1],\
            xyz_all[i,2]

xyz_file.close()

