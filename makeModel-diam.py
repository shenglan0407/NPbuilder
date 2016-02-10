import math


# atoms in each cell

a      = 5.43095 # lattice spacing for silicon
atomID = 14
a1     = (       0.0,       0.0,      0.0  )
a2     = (       0.0,  a*(2/4.),  a*(2/4.) )
a3     = (  a*(2/4.),       0.0,  a*(2/4.) )
a4     = (  a*(2/4.),  a*(2/4.),      0.0  )
a5     = (  a*(3/4.),  a*(3/4.),  a*(3/4.) )
a6     = (  a*(3/4.),  a*(1/4.),  a*(1/4.) )
a7     = (  a*(1/4.),  a*(3/4.),  a*(1/4.) )
a8     = (  a*(1/4.),  a*(1/4.),  a*(3/4.) )

atoms         = ( a1, a2, a3, a4, a5, a6, a7 ,a8 ) 

n_atoms       = len( atoms )

size_in_nm    = float ( input("size [diameter] in nm: " ) ) 

size_in_ang   = size_in_nm * 10.

center        = ( size_in_ang / 2., size_in_ang / 2., size_in_ang / 2. )

out_file_name = 'diam_sphere_'+ str( size_in_nm) + 'nm.coor'

out_file      = open( out_file_name,'w')


u1 = 0
while u1 < size_in_ang:
    u2 = 0
    while u2 < size_in_ang:
        u3 = 0
        while u3 < size_in_ang:        
            i = 0
            while i < n_atoms :
                atomX = u1 + atoms[i][0]
                atomY = u2 + atoms[i][1]
                atomZ = u3 + atoms[i][2]
                radius = math.sqrt( ( atomX - center[0] )**2 + \
                                  ( atomY - center[1] )**2 + \
                                  ( atomZ - center[2] )**2  ) 
                if radius <= size_in_ang / 2:
                    print >> out_file , atomX,atomY,atomZ,atomID
                i += 1
            u3 += a
        u2 += a
    u1 += a

out_file.close()

print "wrote file", 'diam_sphere_'+ str( size_in_nm) + 'nm.coor' ,"."
