# -*- coding: utf-8 -*-
from pylab import *
import os

# MET grib2 pre_preocess

# [1] wgrib2 gfs.grib2  -new_grid latlon 70:280:0.25 0:240:0.25 gfs.regrid_china.grb2

# [2] wgrib2 gfs.regrid_china.grb2 -netcdf gfs.regrid_china.nc

# [3]  plot_data_plane  gfs.regrid_china.grb2  test.ps 'name="HGT";level="P500";'

# [4]  pop_combine -add     gfs.2018061812_f018.regrid_china.grb2 6 \
#                           gfs.2018061812_f024.regrid_china.grb2 6 \
#                           gfs.2018061812_f030.regrid_china.grb2 6 \
#                           gfs.2018061812_f036.regrid_china.grb2 6 \
#                           apcp24.gfs.2018061812_f036.nc
#
#
def gfsgrib_regrid2china_proc():

    res=os.popen("ls gfs.2018061712").read()

    grbfname = res.splitlines()

    for grbfile in grbfname:

        cmd1 = "cp ./gfs.2018061712/"+grbfile + " ./gfs.grb2 "

        desfile = "gfs.2018061712_" + grbfile[20:24] +".regrid_china.grb2"

        cmd2 = "wgrib2 gfs.grb2  -new_grid latlon 70:280:0.25 0:240:0.25 " + desfile

        print(cmd1)

        os.system(cmd1)

        print(cmd2)

        os.system(cmd2)


#print("123")


###########################################

def met_getgfs_apcp24( cdate, vhr ):

    vhrs = range(vhr, vhr-24, -6)

    print(vhrs)

    cmd = "pcp_combine -add gfs." + cdate + "_f" + str(vhrs[3]).zfill(3) + ".regrid_china.grb2 6 " +  \
                           "gfs." + cdate + "_f" + str(vhrs[2]).zfill(3) + ".regrid_china.grb2 6 " +  \
                           "gfs." + cdate + "_f" + str(vhrs[1]).zfill(3) + ".regrid_china.grb2 6 " +  \
                           "gfs." + cdate + "_f" + str(vhrs[0]).zfill(3) + ".regrid_china.grb2 6 " +  \
                           " apcp24.gfs." + cdate + "_f" + str(vhr).zfill(3) + ".nc "

    print(cmd)

    os.system(cmd)



###########################################



#gfsgrib_regrid2china_proc()

met_getgfs_apcp24("2018061712", 60)


# print(cmd)


#os.system(cmd)

