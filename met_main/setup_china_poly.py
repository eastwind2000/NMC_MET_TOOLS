# -*- coding: utf-8 -*-
from pylab import *

##################################################



china_poly = file("china.poly","r").readlines()

tempstr = " ".join(china_poly)

points = tempstr.split()

num_points = len(points) / 3

np_points = np.zeros( (num_points, 2)  )

# for i in range( len(points)/3   ):
#
#     j = (i-1)*3
#
#     np_points[i, 0 ] = float( points[i]   )
#
#     np_points[i, 1] = float(points[i])


lon = points[0::3]

lat = points[1::3]

pfile = file("China_boundary.poly", "w")

pfile.write("ChinaPoints_"+str(num_points)+"\n")

for i in range( num_points ):
    linebufr = lat[i] + " " + lon[i] + "\n"
    print(linebufr)
    pfile.write(linebufr)
pfile.close()













