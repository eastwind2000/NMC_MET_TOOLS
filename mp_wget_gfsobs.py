# -*- coding: utf-8 -*-
from pylab import *
import os
import multiprocessing
from multiprocessing import Process


# http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.2018061912/gfs.t12z.adpsfc.tm00.bufr_d.nr

# http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.2018061912/gfs.t12z.adpupa.tm00.bufr_d

# get information of prebufr data

# pb2nc. /gfsobs/gfs_2018062000.adpsfc.bufr_d.nr   sfcobs_test.nc   config_pb2nc


def wgetdata(cmd):
    print(cmd)
    os.system(cmd)


# cdate = ["2018061800",
#          "2018061812",
#          "2018061900",
#          "2018061912",
#          "2018062000",
#          "2018062012",
#          "2018062100",
#          "2018062112"]

cdate = ["2018062006",
         "2018062018",
         "2018062106",
         "2018062118",
         "2018062512",
         "2018062518",
         "2018062600",
         "2018062606"
         ]

for idate in cdate:

    sfclink  = "http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs."+idate+"/gfs.t"+ idate[-2::] +"z.adpsfc.tm00.bufr_d.nr"

    upalink = "http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs."+idate+"/gfs.t"+ idate[-2::] +"z.adpupa.tm00.bufr_d"

#################

    cmd = " wget -c " + sfclink + " -O  " + "gfs_"+idate+".adpsfc.bufr_d.nr"

    px = Process( target=wgetdata, args=(cmd, ) )

    px.start()

#################

    cmd =  " wget -c " + upalink + "    -O  " + "gfs_"+idate+".adpupa.bufr_d"

    px = Process( target=wgetdata, args=(cmd, ) )

    px.start()

