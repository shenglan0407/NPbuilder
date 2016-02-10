
"""
Generate simple toy models that are simple 2-d shapes (pentagons, squares, etc)
made up of gold atoms. Useful for testing simple theories.
"""

import numpy as np

atomic_number = 79 # 79 = gold
radius = 4.0 # angstroms

n_vertices = int( raw_input('Enter the number of verticies you want the system'
                            ' to have (e.g. 5=pentagon): ') )

phi = 2.0 * np.pi / float(n_vertices)

coord = np.zeros((n_vertices, 4))

for n in range(n_vertices):    
    x = radius * np.cos(n * phi)
    y = radius * np.sin(n * phi)
    coord[n,:] = np.array([x, y, 0.0, atomic_number])
    
output_fn = 'planar-%dvert.coor' % n_vertices
np.savetxt(output_fn, coord, fmt='%.3f')
print "Saved: %s" % output_fn
