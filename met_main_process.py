# -*- coding: utf-8 -*-
from pylab import *

import os

import datetime

import met_setup_obs_micaps

import met_setup_ec_fcst

import met_setup_obs_qpe

import global_vars as gv

#

# [1] Setting up obs-validate, basic variants

# [2] reading Micaps r24-88 file

# [3] reading CMORPH QPE24

# [4] reading nwp forecast precipitation

# [5] reading satellite-obs? IR/WV

# [6] point_stat EC/NCEP/...

# [7] MODE EC/NCEP/...

# [8] timecycle

#############################################

cdate_utc = "2018062900"    # obs-valid time in UTC

cyear = cdate_utc[0:4]

cmon = cdate_utc[4:6]

cday = cdate_utc[6:8]

chour = cdate_utc[8:10]

print(cyear + cmon + cday + chour)

utcdate = datetime.datetime(int(cyear), int(cmon),int(cday), int(chour) )

lstdate = utcdate + datetime.timedelta(hours=8)

cdate_lst = lstdate.strftime("%Y%m%d%H")     # obs-valid time in lST-Beijing

print
print(" =================================== ")
print

print( "  Time UTC  ==  " + cdate_utc  )
print( "  Time LST  ==  " + cdate_lst  )

######################################################
# [2.1] Readding micaps r24-88 file

met_setup_obs_micaps.setup_data( cdate_utc, cdate_lst )

# [2.2] Readding CMORPH QPE

met_setup_obs_qpe.setup_obs_qpe(cdate_utc)

######################################################
# [4.1] Reading NWP-ECMWF forecast precipitation

for vhr in arange(24, 12*9, 12):     # [24, 36, 48, 72, 96]

    initnwp_date = utcdate - datetime.timedelta(hours=vhr)

    cdate_initnwp = initnwp_date.strftime("%Y%m%d%H")  # nwp-mode inittime

    print( " NWP_INIT:  "  +   cdate_initnwp + " ==> + " + str(vhr) + "H  " + cdate_utc )

    met_setup_ec_fcst.setup_ec_fcst  ( cdate_initnwp, vhr, cdate_utc )

# [4.2] Reading NWP-GFS forecast precipitation


# [4.3] Reading NWP-GRAPES forecast precipitation



################ MET_EXEC ######################################

# [6] MET_TOOLS for precipitation forecasting

## [6.1] Setting up products inventory

desdir = gv.result_dir + "ecmwf/" + cdate_utc
os.system("mkdir -p " + desdir)

## [6.2] Execute MET_TOOLS command

m4_obs_file = gv.result_dir + "micaps" + "_r24_" + cdate_utc + ".nc"

qpe_obs_file = gv.result_dir + "cpc_cmorph_china_" + cdate_utc  + ".nc"

for vhr in arange(24, 12*9, 12):

    initnwp_date = utcdate - datetime.timedelta(hours=vhr)

    cdate_initnwp = initnwp_date.strftime("%Y%m%d%H")  # nwp-mode inittime

    fcst_file = gv.result_dir + "ecmwf_r24_" + cdate_initnwp + "_f" + str(vhr).zfill(3) + ".nc"

    ##################

    cmd= "point_stat " + fcst_file + " " + m4_obs_file + " config_pointstat_ecmwf.h "
    print
    print(cmd)
    os.system( cmd )
    os.system(" mv  point_stat_* " + desdir)
    print( " =============================================  ")

    cmd = "mode " + fcst_file + " " + qpe_obs_file + " config_mode_ecmwf.h "
    print
    print(cmd)
    os.system(cmd)
    os.system(" mv  mode_* " + desdir)
    print(" =============================================  ")

    cmd = "grid_stat " + fcst_file + " " + qpe_obs_file + " config_gridstat_ecmwf.h "
    print
    print(cmd)
    os.system(cmd)
    os.system(" mv  grid_stat* " + desdir)
    print(" =============================================  ")

############################################


