# -*- coding: utf-8 -*-
from pylab import *

import os

import datetime

from met_setup_obs_micaps import *

from met_setup_fcst import *

from met_postproc import *

from met_setup_obs_qpe import *

from global_vars_linux import *

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

cdate_utc_list = ["2018071400",
                  "2018071500",
                  "2018071600",
                  "2018071700",
                  "2018071800",
                  "2018071900",
                  "2018072000",
                  "2018072100",
                  "2018072200",
                  "2018072300",
                  "2018072400",
                  "2018072500",
                  "2018072600",
                  "2018072700",
                  "2018072800",
                  "2018072900",
                  "2018073000",
                  "2018073100" ]


for cdate_utc in cdate_utc_list:

    # met_postproc(cdate_utc)
    #
    # pdb.set_trace()

    cyear = cdate_utc[0:4]

    cmon = cdate_utc[4:6]

    cday = cdate_utc[6:8]

    chour = cdate_utc[8:10]

    print(cyear + cmon + cday + chour)

    utcdate = datetime.datetime(int(cyear), int(cmon), int(cday), int(chour))

    lstdate = utcdate + datetime.timedelta(hours=8)

    cdate_lst = lstdate.strftime("%Y%m%d%H")  # obs-valid time in lST-Beijing

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

    setup_cmorph_qpe(cdate_utc)

    m4_obs_file = result_dir + "micaps" + "_r24_" + cdate_utc + ".nc"

    qpe_obs_file = result_dir + "cpc_cmorph_china_" + cdate_utc + ".nc"

    ######################################################

    # [4.3]

    # pdb.set_trace()

    # [4.1]

    for vhr in arange(24, 12 * 8, 12):  # [24, 36, 48, 60, 72, 84]

        initnwp_date = utcdate - datetime.timedelta(hours=vhr)

        cdate_initnwp = initnwp_date.strftime("%Y%m%d%H")  # nwp-mode inittime

        print(" NWP_INIT:  " + cdate_initnwp + " ==> + " + str(vhr) + "H  " + cdate_utc)

        ## Reading NWP-ECMWF forecast precipitation

        if (use_ecmwf):
            setup_ec_fcst(cdate_initnwp, vhr, cdate_utc)

        ## Reading NWP-GFS forecast precipitation

        if (use_gfs):
            setup_gfs_fcst(cdate_initnwp, vhr, cdate_utc)

        ## Reading NWP-WARMS from ShangHai-WFO forecast precipitation

        if (use_warms and vhr <= 48):
            setup_warms_fcst(cdate_initnwp, vhr, cdate_utc)

        ## setup ECMWF_EPS forecast precipitation

        if (use_eceps):
            setup_eceps_fcst(cdate_initnwp, vhr, cdate_utc)

    ################ MET_EXEC ######################################

    # [6] call MET_TOOLS commands for precipitation verification

    ## [6.1] Setting up products inventory

    # nwpfcst = ["ecmwf", "gfs", "warms", "eceps"]

    nwpfcst = ["ecmwf", "gfs", "warms"]

    for model in nwpfcst:

        if (model == "ecmwf" or model == "gfs" or model == "eceps"):
            fcst_length = 12 * 8

        if (model == "warms"):
            fcst_length = 12 * 5

        desdir = result_dir + model + "/" + cdate_utc + "/"

        os.system("mkdir -p " + desdir)

        ## [6.2] Execute MET_TOOLS command

        for vhr in arange(24, fcst_length, 12):

            initnwp_date = utcdate - datetime.timedelta(hours=vhr)

            cdate_initnwp = initnwp_date.strftime("%Y%m%d%H")  # nwp-mode inittime

            fcst_file = result_dir + model + "_r24_" + cdate_initnwp + "_f" + str(vhr).zfill(3) + ".nc"

            # met_postproc(cdate_initnwp, vhr, cdate_utc)  # post_progress for met output

            # pdb.set_trace()

            ##################

            cmd = "point_stat " + fcst_file + " " + m4_obs_file \
                  + " config_pointstat_" + model + ".h" \
                  + " -outdir " + desdir

            print
            print(cmd)
            os.system(cmd)
            print("=" * 40)

            cmd = "grid_stat " + fcst_file + " " + qpe_obs_file \
                  + " config_gridstat_" + model + ".h" \
                  + " -outdir " + desdir
            print
            print(cmd)
            os.system(cmd)
            # os.system(" mv  grid_stat* " + desdir)
            print("=" * 40)

            cmd = "mode " + fcst_file + " " + qpe_obs_file \
                  + " config_mode_" + model + ".h" \
                  + " -outdir " + desdir
            print
            print(cmd)
            os.system(cmd)

            # print("=" * 40)
            # cmd = "wavelet_stat " + fcst_file + " " + qpe_obs_file + " config_wavelet_" + model + ".h"
            # print
            # print(cmd)
            # os.system(cmd)
            # os.system(" mv  wavelet_* " + desdir)
            # print("=" * 40)

            if (model == "eceps"):
                eps_fcst_files = "../MET_RESULT/eceps_r24_ens*_" + cdate_initnwp + "_f" + str(vhr).zfill(3) + ".nc"

                cmd = "ensemble_stat 51 " + eps_fcst_files \
                      + " config_ensemblestat_eceps.h " \
                      + " -point_obs " + m4_obs_file \
                      + " -outdir " + desdir
                print(cmd)
                os.system(cmd)

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

    ###############################################

    # [7.0] Setting up MET_postproc

    met_postproc(cdate_utc)  # post_progress for met output

    #
    #






