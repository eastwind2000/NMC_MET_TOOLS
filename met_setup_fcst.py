# -*- coding: utf-8 -*-
from pylab import *

import os

import time

import datetime

from netCDF4 import Dataset

import global_vars as gv

import pdb


def setup_eceps_fcst(init_cdate, vhr, valid_cdate):  # datafile error from nwp-database

    nens = 51

    tempvar = datetime.datetime(int(init_cdate[0:4]),
                                int(init_cdate[4:6]),
                                int(init_cdate[6:8]),
                                int(init_cdate[8:10]) ) + datetime.timedelta(hours=8)    ## very tricky, why use LST time !

    init_unixtime = time.mktime( tempvar.utctimetuple() )      ## change to unix-time-stample

    tempvar = datetime.datetime(int( valid_cdate[0:4] ),
                                int( valid_cdate[4:6] ),
                                int( valid_cdate[6:8] ),
                                int( valid_cdate[8:10]) ) + datetime.timedelta(hours=8)   ## very ticky, why need to use LST time !

    valid_unixtime = time.mktime( tempvar.utctimetuple())

    fdir = gv.nwp_eceps_dir + init_cdate  + "/"

    apcp24_fname = fdir + "ecmfEnsemble_IT_" + init_cdate      \
                                 +   "_VT_" + valid_cdate     \
                                 +   "_FH_" + str(vhr).zfill(3)  +  "_AT_024.nc"
    print(apcp24_fname)

    ncdata = Dataset(apcp24_fname, "r")

    lon = ncdata.variables["longitude"][:]  # masked array difference under windows & linux

    lat = ncdata.variables["latitude"][:]  # masked array

    nlat = len(lat)

    nlon = len(lon)

    tp = ncdata.variables["tp"][:, 0, 0, :, :].data  # total precipitation masked-array

    for iens in range(nens):

        print(["shape of TP in ncfiles  : ", shape(tp)])

        ########################### draw temperoy figure ############

        # figure(1)
        #
        # contourf(tp.reshape((nlat, nlon)), cmap=cm.summer, levels=linspace(0, 300, 30))
        #
        # colorbar()

        # pdb.set_trace()

        #############################################################

        s00 = "netcdf eceps_r24_"  + "ENS" + str(iens).zfill(2) + "_" + init_cdate + "_f" + str(vhr).zfill(3) + " {" + "\n"

        s01 = "dimensions: " + "\n" + \
              " lat = 601; " + "\n" + \
              " lon = 701; " + "\n"

        s02 = "variables:  "                                                                                         + "\n" + \
              "float lat(lat) ; "                                                                                    + "\n" + \
              "   lat:long_name = \"latitude\" ;"                                                                    + "\n" + \
              "   lat:units = \"degrees_north\" ;"                                                                   + "\n" + \
              "   lat:standard_name = \"latitude\" ;"                                                                + "\n" + \
              "float lon(lon) ;"                                                                                     + "\n" + \
              "   lon:long_name = \"longitude\" ;"                                                                   + "\n" + \
              "   lon:units = \"degrees_east\" ;"                                                                    + "\n" + \
              "   lon:standard_name = \"longitude\" ;"                                                               + "\n" + \
              "float APCP_24(lat, lon) ;"                                                                            + "\n" + \
              "   APCP_24:name = \"APCP_24\" ;"                                                                      + "\n" + \
              "   APCP_24:long_name = \"Total Precipitation\" ;"                                                     + "\n" + \
              "   APCP_24:level = \"A24\" ;"                                                                         + "\n" + \
              "   APCP_24:units = \"kg/m^2\" ;"                                                                      + "\n" + \
              "   APCP_24:_FillValue = -9999.f ;"                                                                    + "\n" + \
              "   APCP_24:init_time = \"" + init_cdate[0:8] + "_" + init_cdate[8:10] + "0000" + "\" ;"               + "\n" + \
              "   APCP_24:init_time_ut = \"" + str(init_unixtime) + "\" ;"                                           + "\n" + \
              "   APCP_24:valid_time = \"" + valid_cdate[0:8] + "_" + valid_cdate[8:10] + "0000" + "\" ;"            + "\n" + \
              "   APCP_24:valid_time_ut = \"" + str(valid_unixtime) + "\" ;"                                         + "\n" + \
              "   APCP_24:accum_time = \"240000\" ;"                                                                 + "\n" + \
              "   APCP_24:_FillValue = 65535 ;"                                                                      + "\n" + \
              "   APCP_24:accum_time_sec = 86400 ;"                                                                  + "\n"

        s03 = " // global attributes: "                                     + "\n" + \
              " :_NCProperties = \"version=1|netcdflibversion=4.4.1.1\" ;"  + "\n" + \
              "	:FileOrigins = \"ECEPS_APCP24\" ; "                         + "\n" + \
              "	:MET_version = \"V7.0\" ;"                                  + "\n" + \
              "	:Projection = \"LatLon\" ;"                                 + "\n" + \
              "	:lat_ll = \"0.0 degrees_north\" ; "                         + "\n" + \
              "	:lon_ll = \"70.0 degrees_east\" ; "                         + "\n" + \
              "	:delta_lat = \"0.10 degrees\" ;"                            + "\n" + \
              "	:delta_lon = \"0.10 degrees\" ;"                            + "\n" + \
              "	:Nlat = \"" + str(nlat) + " grid_points\" ; "               + "\n" + \
              "	:Nlon = \"" + str(nlon) + " grid_points\" ; "               + "\n"

        s04 = "data:" + "\n"

        s05 = "lat = " + ",".join(str(item) for item in lat) + ";\n"

        s06 = "lon = " + ",".join(str(item) for item in lon) + ";\n"

        s07 = "APCP_24 = " + ",".join(str(item) for item in tp[iens, :, :].flatten()) + ";\n"

        s0x = " } \n"

        #############################################################

        im_ncfname = gv.result_dir + "im_eceps" + "ens" + str(iens).zfill(2) +"_ncfile.cdl"

        im_ncfile = open(im_ncfname, "wb")

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

        out_ncfile = gv.result_dir + "eceps_r24_" + "ens" + str(iens).zfill(2) + "_"  + init_cdate + "_f" + str(vhr).zfill(3) + ".nc"

        print

        cmd = "ncgen  -o " + out_ncfile + " " + im_ncfname

        print(cmd)
        os.system(cmd)

        cmd = "ncdump -h " + out_ncfile
        print(cmd)
        os.system(cmd)

        print

    print("#"*40)


########################################################################################################################


def setup_warms_fcst(init_cdate, vhr, valid_cdate):  # datafile error from nwp-database

    tempvar = datetime.datetime(int(init_cdate[0:4]),
                                int(init_cdate[4:6]),
                                int(init_cdate[6:8]),
                                int(init_cdate[8:10]) ) + datetime.timedelta(hours=8)    ## very tricky, why use LST time !

    init_unixtime = time.mktime( tempvar.utctimetuple() )      ## change to unix-time-stample

    tempvar = datetime.datetime(int( valid_cdate[0:4] ),
                                int( valid_cdate[4:6] ),
                                int( valid_cdate[6:8] ),
                                int( valid_cdate[8:10]) ) + datetime.timedelta(hours=8)   ## very ticky, why use LST time !

    valid_unixtime = time.mktime( tempvar.utctimetuple() )

    fdir = gv.nwp_warms_dir + init_cdate  + "/"

    apcp24_fname = fdir + "mesoSHANGHAI_IT_" + init_cdate      \
                                 +   "_VT_" + valid_cdate     \
                                 +   "_FH_" + str(vhr).zfill(3)  +  "_AT_024.nc"
    print(apcp24_fname)

    ncdata = Dataset(apcp24_fname, "r")

    lon = ncdata.variables["longitude"][:]  # masked array difference under windows & linux

    lat = ncdata.variables["latitude"][:]  # masked array

    tp = ncdata.variables["tp"][:][0, 0, :, :].data   # total precipitation masked-array


    nlat = len(lat)

    nlon = len(lon)

    print( ["shape of TP in ncfiles  : ",  shape(tp)] )

    ########################### draw temperoy figure ############

    # figure(1)
    #
    # contourf(tp.reshape((nlat, nlon)), cmap=cm.summer, levels=linspace(0, 300, 30))
    #
    # colorbar()

    # pdb.set_trace()

    #############################################################

    s00 = "netcdf warms_r24_" + init_cdate + "_f" + str(vhr).zfill(3)  +  " {" + "\n"

    s01 = "dimensions: " + "\n" + \
          " lat = 601; " + "\n" + \
          " lon = 701; " + "\n"

    s02 = "variables:  "                                                                                        + "\n" + \
          "float lat(lat) ; "                                                                                   + "\n" + \
          "   lat:long_name = \"latitude\" ;"                                                                   + "\n" + \
          "   lat:units = \"degrees_north\" ;"                                                                  + "\n" + \
          "   lat:standard_name = \"latitude\" ;"                                                               + "\n" + \
          "float lon(lon) ;"                                                                                    + "\n" + \
          "   lon:long_name = \"longitude\" ;"                                                                  + "\n" + \
          "   lon:units = \"degrees_east\" ;"                                                                   + "\n" + \
          "   lon:standard_name = \"longitude\" ;"                                                              + "\n" + \
          "float APCP_24(lat, lon) ;"                                                                           + "\n" + \
          "   APCP_24:name = \"APCP_24\" ;"                                                                     + "\n" + \
          "   APCP_24:long_name = \"Total Precipitation\" ;"                                                    + "\n" + \
          "   APCP_24:level = \"A24\" ;"                                                                        + "\n" + \
          "   APCP_24:units = \"kg/m^2\" ;"                                                                     + "\n" + \
          "   APCP_24:_FillValue = -9999.f ;"                                                                   + "\n" + \
          "   APCP_24:init_time = \""  + init_cdate[0:8]+"_"+ init_cdate[8:10] + "0000" +  "\" ;"               + "\n" + \
          "   APCP_24:init_time_ut = \"" + str(init_unixtime) + "\" ;"                                          + "\n" + \
          "   APCP_24:valid_time = \"" + valid_cdate[0:8]+ "_"+ valid_cdate[8:10] +"0000"  + "\" ;"             + "\n" + \
          "   APCP_24:valid_time_ut = \"" +  str(valid_unixtime) + "\" ;"                                       + "\n" + \
          "   APCP_24:accum_time = \"240000\" ;"                                                                + "\n" + \
          "   APCP_24:_FillValue = 65535 ;"                                                                     + "\n" + \
          "   APCP_24:accum_time_sec = 86400 ;"                                                                 + "\n"

    s03 = " // global attributes: " + "\n" + \
          " :_NCProperties = \"version=1|netcdflibversion=4.4.1.1\" ;" + "\n" + \
          "	:FileOrigins = \"WARMS_APCP24\" ; " + "\n" + \
          "	:MET_version = \"V7.0\" ;" + "\n" + \
          "	:Projection = \"LatLon\" ;" + "\n" + \
          "	:lat_ll = \"0.0 degrees_north\" ; " + "\n" + \
          "	:lon_ll = \"70.0 degrees_east\" ; " + "\n" + \
          "	:delta_lat = \"0.10 degrees\" ;" + "\n" + \
          "	:delta_lon = \"0.10 degrees\" ;" + "\n" + \
          "	:Nlat = \"" + str(nlat) + " grid_points\" ; " + "\n" + \
          "	:Nlon = \"" + str(nlon) + " grid_points\" ; " + "\n"

    s04 = "data:" + "\n"

    s05 = "lat = " + ",".join(str(item) for item in lat) + ";\n"

    s06 = "lon = " + ",".join(str(item) for item in lon) + ";\n"

    s07 = "APCP_24 = " + ",".join(str(item) for item in tp.flatten()) + ";\n"

    s0x = " } \n"

    #############################################################

    im_ncfile_name = gv.result_dir + "im_warms_ncfile.cdl"

    im_ncfile = open(im_ncfile_name, "wb")

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

    out_ncfile_name = gv.result_dir + "warms_r24_" + init_cdate  + "_f" + str(vhr).zfill(3) + ".nc"

    print

    cmd = "ncgen  -o " + out_ncfile_name + " " + im_ncfile_name
    print(cmd)
    os.system(cmd)

    cmd = "ncdump -h " + out_ncfile_name
    print(cmd)
    os.system(cmd)

    print


########################################################################################################################

def setup_gfs_fcst(init_cdate, vhr, valid_cdate):

    tempvar = datetime.datetime(int(init_cdate[0:4]),
                                int(init_cdate[4:6]),
                                int(init_cdate[6:8]),
                                int(init_cdate[8:10]) ) + datetime.timedelta(hours=8)    ## very tricky, why use LST time !

    init_unixtime = time.mktime( tempvar.utctimetuple() )      ## change to unix-time-stample

    tempvar = datetime.datetime(int( valid_cdate[0:4] ),
                                int( valid_cdate[4:6] ),
                                int( valid_cdate[6:8] ),
                                int( valid_cdate[8:10]) ) + datetime.timedelta(hours=8)   ## very ticky, why use LST time !

    valid_unixtime = time.mktime( tempvar.utctimetuple() )


    fdir = gv.nwp_gfs_dir + init_cdate  + "/"

    apcp24_fname = fdir + "globalNCEP_IT_" + init_cdate      \
                                 +   "_VT_" + valid_cdate     \
                                 +   "_FH_" + str(vhr).zfill(3)  +  "_AT_024.nc"

    print(apcp24_fname)

    ncdata = Dataset(apcp24_fname, "r")

    lon = ncdata.variables["longitude"][:]  # masked array difference under windows & linux

    lat = ncdata.variables["latitude"][:]  # masked array

    tp = ncdata.variables["tp"][:][0, 0, :, :].data   # total precipitation masked-array

    nlat = len(lat)

    nlon = len(lon)

    print( ["shape of TP in ncfiles  : ",  shape(tp)] )

    ########################### draw temperoy figure ############

    # figure(1)
    #
    # contourf(tp.reshape((nlat, nlon)), cmap=cm.summer, levels=linspace(0, 300, 30))
    #
    # colorbar()
    #
    # pdb.set_trace()

    #############################################################

    s00 = "netcdf gfs_r24_" + init_cdate + "_f" + str(vhr).zfill(3)  +  " {" + "\n"

    s01 = "dimensions: " + "\n" + \
          " lat = 601; " + "\n" + \
          " lon = 701; " + "\n"

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
          "   APCP_24:init_time = \""  + init_cdate[0:8]+"_"+ init_cdate[8:10] + "0000" +  "\" ;" + "\n" + \
          "   APCP_24:init_time_ut = \"" + str(init_unixtime) + "\" ;" + "\n" + \
          "   APCP_24:valid_time = \"" + valid_cdate[0:8]+ "_"+ valid_cdate[8:10] +"0000"  + "\" ;" + "\n" + \
          "   APCP_24:valid_time_ut = \"" +  str(valid_unixtime) + "\" ;" + "\n" + \
          "   APCP_24:accum_time = \"240000\" ;"   + "\n" + \
          "   APCP_24:_FillValue = 65535 ;"        + "\n" + \
          "   APCP_24:accum_time_sec = 86400 ;"    + "\n"

    s03 = " // global attributes: " + "\n" + \
          " :_NCProperties = \"version=1|netcdflibversion=4.4.1.1\" ;" + "\n" + \
          "	:FileOrigins = \"GFS_HR_APCP24\" ; " + "\n" + \
          "	:MET_version = \"V7.0\" ;" + "\n" + \
          "	:Projection = \"LatLon\" ;" + "\n" + \
          "	:lat_ll = \"0.0 degrees_north\" ; " + "\n" + \
          "	:lon_ll = \"70.0 degrees_east\" ; " + "\n" + \
          "	:delta_lat = \"0.10 degrees\" ;" + "\n" + \
          "	:delta_lon = \"0.10 degrees\" ;" + "\n" + \
          "	:Nlat = \"" + str(nlat) + " grid_points\" ; " + "\n" + \
          "	:Nlon = \"" + str(nlon) + " grid_points\" ; " + "\n"

    s04 = "data:" + "\n"

    s05 = "lat = " + ",".join(str(item) for item in lat) + ";\n"

    s06 = "lon = " + ",".join(str(item) for item in lon) + ";\n"

    s07 = "APCP_24 = " + ",".join(str(item) for item in tp.flatten()) + ";\n"

    s0x = " } \n"

    #############################################################

    im_ncfile_name = gv.result_dir + "im_gfs_ncfile.cdl"

    im_ncfile = open(im_ncfile_name, "wb")

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

    out_ncfile_name = gv.result_dir + "gfs_r24_" + init_cdate + "_f" + str(vhr).zfill(3) + ".nc"

    print

    cmd = "ncgen  -o " + out_ncfile_name + " " + im_ncfile_name
    print(cmd)
    os.system(cmd)

    cmd = "ncdump -h " + out_ncfile_name
    print(cmd)
    os.system(cmd)

    print


########################################################################################################################



def setup_ec_fcst(init_cdate, vhr, valid_cdate):

    # nlat = 601
    # nlon = 701
    # pdb.set_trace()

    tempvar = datetime.datetime(int(init_cdate[0:4]),
                                int(init_cdate[4:6]),
                                int(init_cdate[6:8]),
                                int(init_cdate[8:10]) ) + datetime.timedelta(hours=8)    ## very tricky, why use LST time !

    init_unixtime = time.mktime( tempvar.utctimetuple() )      ## change to unix-time-stample

    tempvar = datetime.datetime(int( valid_cdate[0:4] ),
                                int( valid_cdate[4:6] ),
                                int( valid_cdate[6:8] ),
                                int( valid_cdate[8:10]) ) + datetime.timedelta(hours=8)   ## very ticky, why use LST time !

    valid_unixtime = time.mktime( tempvar.utctimetuple() )


    fdir = gv.nwp_ec_dir + init_cdate  + "/"

    apcp24_fname = fdir + "globalECMWF_IT_" + init_cdate      \
                                 +   "_VT_" + valid_cdate     \
                                 +   "_FH_" + str(vhr).zfill(3)  +  "_AT_024.nc"

    print(apcp24_fname)

    ncdata = Dataset(apcp24_fname, "r")

    lon = ncdata.variables["longitude"][:]  # masked array difference under windows & linux

    lat = ncdata.variables["latitude"][:]  # masked array

    tp = ncdata.variables["tp"][:][0, 0, :, :].data   # total precipitation masked-array

    # pdb.set_trace()

    # print(shape(lat))

    # print(lon)

    nlat = len(lat)

    nlon = len(lon)

    print( ["shape of TP in ncfiles  : ",  shape(tp)] )

    ########################### draw temperoy figure ############

    # figure(1)
    #
    # plt.contourf(tp.reshape((nlat, nlon)), cmap=cm.summer, levels=linspace(0, 300, 30))
    #
    # plt.colorbar()
    #
    # close(figure(1))

    #############################################################

    s00 = "netcdf ecmwf_r24_" + init_cdate + "_f" + str(vhr).zfill(3)  +  " {" + "\n"

    s01 = "dimensions: " + "\n" + \
          " lat = 601; " + "\n" + \
          " lon = 701; " + "\n"

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
          "   APCP_24:init_time = \""  + init_cdate[0:8]+"_"+ init_cdate[8:10] + "0000" +  "\" ;" + "\n" + \
          "   APCP_24:init_time_ut = \"" + str(init_unixtime) + "\" ;" + "\n" + \
          "   APCP_24:valid_time = \"" + valid_cdate[0:8]+ "_"+ valid_cdate[8:10] +"0000"  + "\" ;" + "\n" + \
          "   APCP_24:valid_time_ut = \"" +  str(valid_unixtime) + "\" ;" + "\n" + \
          "   APCP_24:accum_time = \"240000\" ;"   + "\n" + \
          "   APCP_24:_FillValue = 65535 ;"        + "\n" + \
          "   APCP_24:accum_time_sec = 86400 ;"    + "\n"

    s03 = " // global attributes: " + "\n" + \
          " :_NCProperties = \"version=1|netcdflibversion=4.4.1.1\" ;" + "\n" + \
          "	:FileOrigins = \"ECMWF_HR_APCP24\" ; " + "\n" + \
          "	:MET_version = \"V7.0\" ;" + "\n" + \
          "	:Projection = \"LatLon\" ;" + "\n" + \
          "	:lat_ll = \"0.0 degrees_north\" ; " + "\n" + \
          "	:lon_ll = \"70.0 degrees_east\" ; " + "\n" + \
          "	:delta_lat = \"0.10 degrees\" ;" + "\n" + \
          "	:delta_lon = \"0.10 degrees\" ;" + "\n" + \
          "	:Nlat = \"" + str(nlat) + " grid_points\" ; " + "\n" + \
          "	:Nlon = \"" + str(nlon) + " grid_points\" ; " + "\n"

    s04 = "data:" + "\n"

    s05 = "lat = " + ",".join(str(item) for item in lat) + ";\n"

    s06 = "lon = " + ",".join(str(item) for item in lon) + ";\n"

    s07 = "APCP_24 = " + ",".join(str(item) for item in tp.flatten()) + ";\n"

    s0x = " } \n"

    #############################################################

    im_ncfile_name = gv.result_dir + "im_ec_ncfile.cdl"

    im_ncfile = open(im_ncfile_name, "wb")

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

    out_ncfile_name = gv.result_dir + "ecmwf_r24_" + init_cdate + "_f" + str(vhr).zfill(3) + ".nc"

    print
    cmd = "ncgen  -o " + out_ncfile_name + " " + im_ncfile_name
    print(cmd)
    os.system(cmd)

    cmd = "ncdump -h " + out_ncfile_name
    print(cmd)
    # os.system(cmd)

    print
