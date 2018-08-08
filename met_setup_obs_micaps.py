# -*- coding: utf-8 -*-
from pylab import *

import os

# import time
#
# import datetime

import global_vars as gv

import pandas as pd

import pdb

# step 1: reading micaps diamond3 file

def setup_data( cdate_utc, cdate_lst  ):

    # micaps_r24_dir = "H:\\fcst2018\\micaps\\r24\\"

    surobs = np.loadtxt("sta2513.c8", usecols=(0, 1, 2, 3))  # stations list for verification

    r24fname = cdate_lst[2::] + ".000"

    print
    print("  Reading Micaps r24-precipitation file : " + gv.micaps_r24_dir + r24fname )
    print

    r24obs = open(gv.micaps_r24_dir + r24fname).readlines()[11:]   # pay attention to global_vars

    nobs = len(r24obs)

    r24data = np.zeros((nobs, 5))

    for i in range(nobs):
        tmpdata = r24obs[i].split()
        r24data[i, 0] = tmpdata[0]         # pay attention!
        r24data[i, 1] = float(tmpdata[1])
        r24data[i, 2] = float(tmpdata[2])
        r24data[i, 3] = float(tmpdata[3])
        r24data[i, 4] = float(tmpdata[4])

    # step 2: write data using acii2nc_MET format

    f_ascii_name = gv.result_dir + "micaps" + "_r24_" + cdate_utc + ".ascii"

    f_nc_name =    gv.result_dir +  "micaps" + "_r24_" + cdate_utc + ".nc"

    print(f_ascii_name + " == > " + f_nc_name )

    f_ascii = open(f_ascii_name, "w")

    undef = -9999.0

    for i in range(len(surobs)):

        msg = "ADPSFC"

        stid = str( int(surobs[i, 0]))  #

        validtime = cdate_utc[0:8] + "_" + cdate_utc[8:10] + "0000"   #  YYYYMMDD_HH0000  20180620

        clat = str(surobs[i, 2])

        clon = str(surobs[i, 1])

        celev = str(surobs[i, 3])

        vartype = "AccPrecip"

        level = "24"

        hgt = "-9999"

        qc = "NA"

        # for r24id in r24data[:,0]:
        #     if ( stid  = r24id ):
        #         print([stid, r24id, r24data[])

        obsdata = str(0.0)

        for k in range(len(r24data[:, 0])):
            if( stid == str(int(r24data[k, 0])) ):
                obsdata = str(r24data[k, 4])
                # print( [stid, str(int(r24data[k, 0])) ] )

        datarec = [msg, stid, validtime, clat, clon, celev, vartype, level, hgt, qc, obsdata]

        print(datarec)

        # pdb.set_trace()

        f_ascii.writelines(" ".join(datarec) + "\n")

    f_ascii.close()


    # step 3: writing data use NETCDF-format using  "ascii2nc" in MET_TOOLS

    print(" =================================== ")
    print

    cmd = "  ascii2nc " + f_ascii_name + " " + f_nc_name
    print(cmd)
    os.system(cmd)
    print

    print(" =================================== ")
    print

    # step 4: writing data using grads format?


    # pdb.set_trace()

