# -*- coding: utf-8 -*-
from pylab import *
import os
import multiprocessing
from multiprocessing import Process


#http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.2018061812/gfs.t12z.pgrb2.0p25.f000

#fct = int(np.linspace(0, 96, 17))

fct = arange(0, 102, 6)

for i in range(17):

    idx = str( int( fct[i] ) ).zfill(3)

    grbdatalink = "http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.2018061612/gfs.t12z.pgrb2.0p25.f" + idx

    cmd = "wget -c " + grbdatalink

    print(cmd)

    os.system(cmd)


# gfs_upper_obs http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gdas.20180616/gdas.t00z.adpupa.tm00.bufr_d

# gfs_surface_obs http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gdas.20180616/gdas.t00z.adpsfc.tm00.bufr_d.nr






###########################################


def wgetdata(datalink):
    cmd = "wget -c " + datalink
    print(cmd)
#     # os.system(cmd)


# for i in range(17):
#
#     idx  = str(i).zfill(3)
#
#     px = Process(target=wgetdata, args=('ix', ) )
#
#     px.start()

# pool = multiprocessing.Pool(processes=4)
#
# if __name__ == "__main__":
#     pool = multiprocessing.Pool(processes=4)
#     for i in xrange(10):
#         datalink = "hello " + str(i)
#         pool.apply_async(wgetdata, args=(datalink, ))
#
#     pool.close()
#
#     pool.join()

print "Sub-process(es) done."





