# -*- coding: utf-8 -*-
from pylab import *

import os

import datetime, time

import global_vars as gv

import pdb

# filename example: CMORPH_V0.x_RAW_0.25deg-DLY_00Z_20180607  means : 2018060708+24hr Precipitation

# #下载QPE数据
# [getSurfFileByTime]
# userinfo=NMC_YBS_chentao/nmc2421
# saveDir=G:/MUSIC/QPE/
# dataCode=SURF_CMPA_RT_NC
# times=20180716050000



def setup_obs_qpe(cdate_utc):

    # cdate_utc = "2018062600"

    init_cdate = datetime.datetime(int( cdate_utc[0:4] ),
                                int( cdate_utc[4:6] ),
                                int( cdate_utc[6:8] ),
                                int( cdate_utc[8:10]) ) - datetime.timedelta(hours=24)  ## very ticky, why use LST time !

    tempvar = init_cdate + datetime.timedelta(hours=8)

    init_unixtime = time.mktime(tempvar.utctimetuple())

    tempvar = datetime.datetime(int( cdate_utc[0:4] ),
                                int( cdate_utc[4:6] ),
                                int( cdate_utc[6:8] ),
                                int( cdate_utc[8:10]) ) + datetime.timedelta(hours=8)   ## very ticky, why use LST time !

    valid_unixtime = time.mktime( tempvar.utctimetuple() )

    # nlat = 182

    # nlon = 282

    # lat = linspace(15.0 - 0.125, 60.0 + 0.125, nlat)

    # lon = linspace(70.0 - 0.125, 140.0 + 0.125, nlon)

    nlat = 480

    nlon = 1440

    lat = linspace( -60+0.125, 60.0-0.125, nlat)

    lon = linspace(0.125, 360-0.125, nlon)

    ###############################################################

    # qpe_dir = "H:\\fcst2018\\database\QPE\\"

    # qpe_file = open(qpe_dir + "cpc_cmorph_china_2018062000.grd", "rb")

    cmorph_fname =  gv.qpe_dir + "CMORPH_V0.x_RAW_0.25deg-DLY_00Z_"+ init_cdate.strftime("%Y%m%d")

    print("  reading CMOPH QPE :" + cmorph_fname )

    qpe_file = open( cmorph_fname, "rb")

    qpe = np.fromfile(qpe_file, dtype=np.float32, count=nlat * nlon).reshape(nlat, nlon)

    lat_china = lat[300:481]
    lon_china = lon[280:561]
    qpe_china = qpe[300:481, 280:561]

    # plt.contourf( apcp_china, cmap=cm.summer, levels=linspace(0,300,30) )
    # plt.title("CPC_CMORPH" )
    # plt.suptitle("")
    # plt.colorbar()
    # plt.show()

    # pdb.set_trace()

    ################################################################

    s00 = "netcdf QPE_CPC_CMORPH." + cdate_utc + "{" + "\n"

    s01 = "dimensions: " + "\n" + \
          " lat = 180; " + "\n" + \
          " lon = 281; " + "\n"

    s02 = "variables:  " + "\n" + \
          "float lat(lat) ; " + "\n" + \
          "   lat:long_name = \"latitude\" ;" + "\n" + \
          "   lat:units = \"degrees_north\" ;" + "\n" + \
          "   lat:standard_name = \"latitude\" ;" + "\n" + \
          "float lon(lon) ;" + "\n" + \
          "   lon:long_name = \"longitude\" ;" + "\n" + \
          "   lon:units = \"degrees_east\" ;" + "\n" + \
          "   lon:standard_name = \"longitude\" ;" + "\n" + \
          "float APCP_24(lat, lon) ;" + "\n" + \
          "   APCP_24:name = \"APCP_24\" ;" + "\n" + \
          "   APCP_24:long_name = \"Total Precipitation\" ;" + "\n" + \
          "   APCP_24:level = \"A24\" ;" + "\n" + \
          "   APCP_24:units = \"kg/m^2\" ;" + "\n" + \
          "   APCP_24:_FillValue = -9999.f ;" + "\n" + \
          "   APCP_24:init_time = \"" + init_cdate.strftime("%Y%m%d") + "_" + init_cdate.strftime("%H") + "0000" + "\" ;" + "\n" + \
          "   APCP_24:init_time_ut = \"" + str(init_unixtime) + "\" ;" + "\n" + \
          "   APCP_24:valid_time = \"" + cdate_utc[0:8] + "_" + cdate_utc[8:10] + "0000" + "\" ;" + "\n" + \
          "   APCP_24:valid_time_ut = \"" + str(valid_unixtime) + "\" ;" + "\n" + \
          "   APCP_24:accum_time = \"240000\" ;" + "\n" + \
          "   APCP_24:_FillValue = -9.99e8 ;" + "\n" + \
          "   APCP_24:accum_time_sec = 86400 ;" + "\n"


    s03 = " // global attributes: " + "\n" + \
          " :_NCProperties = \"version=1|netcdflibversion=4.4.1.1|hdf5libversion=1.8.12\" ;" + "\n" + \
          "	:FileOrigins = \"CPC_CMORPH_DAILY_PRCP\" ; " + "\n" + \
          "	:MET_version = \"V7.0\" ;" + "\n" + \
          "	:Projection = \"LatLon\" ;" + "\n" + \
          "	:lat_ll = \"15.125 degrees_north\" ; " + "\n" + \
          "	:lon_ll = \"70.125 degrees_east\" ; " + "\n" + \
          "	:delta_lat = \"0.250000 degrees\" ;" + "\n" + \
          "	:delta_lon = \"0.250000 degrees\" ;" + "\n" + \
          "	:Nlat = \"180 grid_points\" ; " + "\n" + \
          "	:Nlon = \"281 grid_points\" ; " + "\n"

    s04 = "data:" + "\n"

    s05 = "lat = " + ",".join(str(item) for item in lat_china) + ";\n"

    s06 = "lon = " + ",".join(str(item) for item in lon_china) + ";\n"

    s07 = "APCP_24 = " + ",".join(str(item) for item in qpe_china.flatten()) + ";\n"

    s0x = " } \n"

    ##################################################

    im_ncfile = open("im_qpe_ncfile.cdl", "wb")

    im_ncfile.write(s00)
    im_ncfile.write(s01)
    im_ncfile.write(s02)
    im_ncfile.write(s03)

    im_ncfile.write(s04)
    im_ncfile.write(s05)
    im_ncfile.write(s06)
    im_ncfile.write(s07)

    im_ncfile.write(s0x)

    im_ncfile.close()

    ################################################

    out_ncfile = gv.result_dir + "cpc_cmorph_china_" + cdate_utc  + ".nc"  # pay attention!

    print

    cmd = "ncgen  -o " + out_ncfile + "  im_qpe_ncfile.cdl "
    print(cmd)
    os.system(cmd)

    cmd = "ncdump -h " + out_ncfile
    print(cmd)
    os.system(cmd)

    print







