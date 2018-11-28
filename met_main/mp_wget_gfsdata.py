# -*- coding: utf-8 -*-
from pylab import *
import os
import multiprocessing
from multiprocessing import Process

def wgetdata(datalink):
    cmd = "wget -c " + datalink
    print(cmd)
    os.system(cmd)

for i in range(17):

    idx  = str(i*6).zfill(3)

    grbdatalink = "http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.2018070312/gfs.t12z.pgrb2.0p25.f" + idx

    px = Process(target=wgetdata, args=(grbdatalink, ) )

    px.start()



