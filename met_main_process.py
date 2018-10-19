# -*- coding: utf-8 -*-
from pylab import *

import os

import datetime

from met_setup_obs_micaps import *

from met_setup_fcst import *

from met_postproc import *

from met_setup_obs_qpe import *

from global_vars_linux import *

from multiprocessing import Process


def met_cmd_exec( cmd  ):
    os.system(cmd)


#

# [1] Setting up obs-validate, basic variants

# [2] reading Micaps r24-88 file

# [3] reading CMORPH QPE24

# [4] reading nwp forecast precipitation

# [5] reading satellite-obs? IR/WV

# [6] point_stat EC/NCEP/...

# [7] MODE EC/NCEP/...

# [8] Timecycle

#############################################

 # obs-valid intercepting time in UTC

# cdate_utc_list = ["2018061300",
#                   "2018061400",
#                   "2018061500",
#                   "2018061600",
#                   "2018061700",
#                   "2018061800",
#                   "2018061900",
#                   "2018062000",
#                   "2018062100",
#                   "2018062200",
#                   "2018062300",
#                   "2018062400",
#                   "2018062500",
#                   "2018062600",
#                   "2018062700",
#                   "2018062800",
#                   "2018062900",
#                   "2018063000",
#                   "2018070100"]

cdate_utc_list = ['']*120

cdate_start = "2018070500"

cdate_end   = "2017090100"

cyear = cdate_start[0:4]
cmon = cdate_start[4:6]
cday = cdate_start[6:8]
chour= cdate_start[8:10]

# pdb.set_trace()

t1 = datetime.datetime(int(cyear), int(cmon), int(cday), int(chour))

# create cdate list

for iday in range(5):

    t2 = t1 + datetime.timedelta(hours=24*iday)

    cdate_utc_list[iday] = t2.strftime("%Y%m%d%H")

    print(cdate_utc_list[iday])

for cdate_utc in cdate_utc_list:

    cyear = cdate_utc[0:4]

    cmon = cdate_utc[4:6]

    cday = cdate_utc[6:8]

    chour = cdate_utc[8:10]

    print(cyear + cmon + cday + chour)

    utcdate = datetime.datetime(int(cyear), int(cmon), int(cday), int(chour))

    lstdate = utcdate + datetime.timedelta(hours=8)

    cdate_lst = lstdate.strftime("%Y%m%d%H")  # obs-valid time in LST-Beijing

    print
    print(" =================================== ")
    print

    cmd = "rm -r -f " + result_dir + "im_*.cdl"
    print(cmd)
    os.system(cmd)

    print("  Time UTC  ==  " + cdate_utc)

    print("  Time LST  ==  " + cdate_lst)

    # for vhr in arange(24, 12*8, 12):     # [24, 36, 48, 60, 72, 84]
    #
    #     initnwp_date = utcdate - datetime.timedelta(hours=vhr)
    #
    #     cdate_initnwp = initnwp_date.strftime("%Y%m%d%H")  # nwp-mode inittime
    #
    #     print("#" * 40)
    #     print( " MET_PostProc :  "  +   cdate_initnwp + " ==> + " + str(vhr) + "H  " + cdate_utc )
    #     print("#" * 40)
    #
    #     met_postproc(cdate_initnwp, vhr, cdate_utc)  # post_progress for met output
    #
    # pdb.set_trace()

    ######################################################
    # [2.1] Readding micaps r24-88 file

    setup_micaps_r24obs(cdate_utc, cdate_lst)

    # [2.2] Readding CMORPH QPE

    # setup_cmorph_qpe(cdate_utc)

    setup_qpe5km_nmic(cdate_utc)

    m4_obs_file = result_dir + "micaps" + "_r24_" + cdate_utc + ".nc"

    # qpe_obs_file = result_dir + "cpc_cmorph_china_" + cdate_utc + ".nc"

    qpe_obs_file = result_dir + "qpe5km_nmic_" + cdate_utc + ".nc"

    ######################################################

    # [4.1]

    for model_name in model_dir:

        fcst_length = model_fcst_length[model_name]

        desdir = result_dir + model_name + "/" + cdate_utc + "/"

        os.system("mkdir -p " + desdir)

        for vhr in arange(24, fcst_length + 12, 12):  # [24, 36, 48, 60, 72, 84]

            initnwp_date = utcdate - datetime.timedelta(hours=vhr)

            cdate_initnwp = initnwp_date.strftime("%Y%m%d%H")  # nwp-mode inittime

            print(" NWP_INIT:  " + cdate_initnwp + " ==> + " + str(vhr) + "H  " + cdate_utc)

            ## Reading NWP-ECMWF forecast precipitation

            if (model_name == "ecmwf"):
                setup_ecmwf_fcst(cdate_initnwp, vhr, cdate_utc)

            ## Reading NWP-GFS forecast precipitation

            if (model_name == "gfs"):
                setup_gfs_fcst(cdate_initnwp, vhr, cdate_utc)

            ## Reading NWP-WARMS from ShangHai-WFO forecast precipitation

            if (model_name == "warms"):
                setup_warms_fcst(cdate_initnwp, vhr, cdate_utc)

            ## setup ECMWF_EPS forecast precipitation

            if (model_name == "eceps"):
                setup_eceps_fcst(cdate_initnwp, vhr, cdate_utc)

            if (model_name == "pwafs15"):
                setup_pwafs15_fcst(cdate_initnwp, vhr, cdate_utc)
                # pdb.set_trace()

            if (model_name == "pwafs03"):
                setup_pwafs03_fcst(cdate_initnwp, vhr, cdate_utc)
                # pdb.set_trace()

            fcst_file = result_dir + model_name + "_r24_" + cdate_initnwp + "_f" + str(vhr).zfill(3) + ".nc"

            ################ MET_EXEC ######################################

            # [6] call MET_TOOLS commands for precipitation verification


            cmd = "point_stat " + fcst_file + " " + m4_obs_file  + \
                                 " config_pointstat_" + model_name + ".h" + " -outdir " + desdir
            print
            print(cmd)

            # pdb.set_trace()
            px = Process(target=met_cmd_exec, args=(cmd, ))
            px.start()
            print("=" * 40)


            cmd = "grid_stat " + fcst_file + " " + qpe_obs_file + \
                     " config_gridstat_" + model_name + ".h" +  " -outdir " + desdir
            print
            print(cmd)
            px = Process(target=met_cmd_exec, args=(cmd,))
            px.start()
            print("=" * 40)


            cmd = "mode " + fcst_file + " " + qpe_obs_file \
                  + " config_mode_" + model_name + ".h" + " -outdir " + desdir
            print
            print(cmd)
            px = Process(target=met_cmd_exec, args=(cmd, ))
            px.start()

            # print("=" * 40)
            # cmd = "wavelet_stat " + fcst_file + " " + qpe_obs_file + " config_wavelet_" + model + ".h"
            # print
            # print(cmd)
            # os.system(cmd)
            # os.system(" mv  wavelet_* " + desdir)
            # print("=" * 40)

            if (model_name == "eceps"):
                eps_fcst_files = "../MET_RESULT/eceps_r24_ens*_" + cdate_initnwp + "_f" + str(vhr).zfill(3) + ".nc"

                cmd = "ensemble_stat 51 " + eps_fcst_files  + " config_ensemblestat_eceps.h " \
                      + " -point_obs " + m4_obs_file  + " -outdir " + desdir
                print(cmd)
                px = Process(target=met_cmd_exec, args=(cmd,))
                px.start()

                f1 = "ensemble_stat_ECEPS_" + cdate_utc[0:8] + "_" + cdate_utc[8:10] + "0000V.stat"
                f2 = "ensemble_stat_ECEPS_" + cdate_utc[0:8] + "_" + cdate_utc[8:10] + "0000V_ens.nc"
                f3 = "ensemble_stat_ECEPS_" + cdate_utc[0:8] + "_" + cdate_utc[8:10] + "0000V_orank.txt"
                f4 = "ensemble_stat_ECEPS_" + cdate_utc[0:8] + "_" + cdate_utc[8:10] + "0000V_phist.txt"
                f5 = "ensemble_stat_ECEPS_" + cdate_utc[0:8] + "_" + cdate_utc[8:10] + "0000V_relp.txt"
                f6 = "ensemble_stat_ECEPS_" + cdate_utc[0:8] + "_" + cdate_utc[8:10] + "0000V_rhist.txt"
                f7 = "ensemble_stat_ECEPS_" + cdate_utc[0:8] + "_" + cdate_utc[8:10] + "0000V_ssvar.txt"

                for fx in [f1, f2, f3, f4, f5, f6, f7]:
                    ifx = fx[0:20] + str(vhr).zfill(3) + "F_" + fx[20::]
                    cmd = "mv " + desdir + fx + " " + desdir + ifx
                    print(cmd)
                    os.system(cmd)

                print("=" * 40)



        px.join()

        print( "Process Start: " + model_name + str(vhr))




    ###############################################

    # [7.0] Setting up MET_postproc

    met_postproc_poinstat(cdate_utc)  # post_progress for met output

    # met_postproc_mode(cdate_utc)


