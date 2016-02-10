from numpy import *
# makes/rotates pyramid with tip at 0,0,0
# and with the base as the x-y plane

def gen_mat(u,v):
    """
    http://stackoverflow.com/questions/9423621/3d-rotations-of-a-plane

    Let u be a normal to plane P1
    Let v be a normal to plane P2

    This function returns the matrix 
    which rotates and point in P1 to 
    a corresponding point in P2
    """
    norm_uv = cross( u,v)
    norm_uv /= linalg.norm(norm_uv)

    rot_ang = arccos( dot( [0,0,1.], norm_uv)) 
    
    assert( not all( array([0,0,1.]) == norm_uv ) )

    rot_axis = cross( [0,0,1], norm_uv )
    rot_axis /= linalg.norm( rot_axis)
    
    c = cos(rot_ang)
    s = sin(rot_ang) 
    c_ = 1-c

    x = rot_axis[0]
    y = rot_axis[1]
    z = rot_axis[2]
    M1 = [ x*x*c_+c, x*y*c_-z*s, x*z*c_+y*s ]
    M2 = [ y*x*c_+z*s, y*y*c_+c, y*z*c_-x*s ]
    M3 = [ z*x*c_-y*s, z*y*c_+x*s, z*z*c_+c ]
    M = array( [M1,M2,M3] ) 

    return M

# args
u = [ .5, -.5*sqrt(3), 0 ]
v = [ .5, .5/sqrt(3), sqrt(6)/3. ] 
rotM = gen_mat(u,v)

# gold unit
a = 4.076
spacing = a/2.

# size of the thing
length = 20 #argparse bla bla
nrows,ncols = length*3,length*3
xcor = [a*i/2. for i in xrange(nrows)]
ycor = [a*i/2. for i in xrange(ncols)]

centerx = xcor[nrows/2]
centery = ycor[ncols/2]

# make a mask of
# 1 0 1 0 1 0 ..
# 0 1 0 1 0 1 ..
# 1 0 1 0 1 0 
# . etc
#
mask = zeros( (nrows, ncols))
mask[::2,1::2] = 1
mask[1::2,0::2] = 1
mask = mask.astype(bool)

# make coordinates of {100} planes when looking down the 
# {100} axis , i.e. at the  base
xyzmap = array( [  [xcor[i], ycor[j], 0] 
        for i in xrange(nrows) for j in xrange(ncols)] )
xyzmap = xyzmap.reshape( (nrows, ncols, 3))

# center the base at x,y = 0,0
xyzmap[:,:,0] -= centerx
xyzmap[:,:,1] -= centery

atoms = []
for i_plane in xrange( length/2 ):
    ii = 2*i_plane
    
    x1,x2 =  (nrows-ii)/2, (nrows+ii)/2 +1 
    y1,y2 = (ncols-ii)/2, (ncols+ii)/2 +1 
    if i_plane%2 == 0:
        m = mask[x1:x2, y1:y2]
    else:
        m = ~mask[x1:x2, y1:y2]
    
    xyz = xyzmap[ x1:x2, y1:y2][m]
    xyz[:,2] = spacing * i_plane
    atoms.extend(xyz)

atoms_txt = [ 'Au ' + ' '.join(map(str,a)) 
            for a in atoms]
savetxt('atoms.xyz',atoms_txt, fmt='%s')

atoms_rot = map( lambda x: dot(rotM,x) , atoms)
atoms_rot_txt = [ 'Au ' + ' '.join(map(str,a)) 
            for a in atoms_rot]
savetxt('atoms_rot.xyz',atoms_rot_txt, fmt='%s')

