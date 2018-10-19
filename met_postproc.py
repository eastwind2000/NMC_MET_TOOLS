# -*- coding: utf-8 -*-
from pylab import *

import os

import datetime

import pandas as pd

import pdb

import  global_vars_linux as gv


#############################################################




def met_postproc_gridstat(cdate_utc):    # post-progressing for grid_stat verification products




    return


#############################################################


def met_postproc_mode(cdate_utc):  # post-progressing for MODE verification products, especially for the Postscript figs.

#    MET_RESULT/ecmwf/2017050100/mode_EC_CMORPH_720000L_20170501_000000V_240000A_R6_T6.ps

    # cdate_utc = "2018062500"

    cyear = cdate_utc[0:4]

    cmon = cdate_utc[4:6]

    cday = cdate_utc[6:8]

    chour = cdate_utc[8:10]

    print(cyear + cmon + cday + chour)

    utcdate = datetime.datetime(int(cyear), int(cmon), int(cday), int(chour))

    # lstdate = utcdate + datetime.timedelta(hours=8)

    print
    print(" =================================== ")
    print

    for model_name in model_dir:

        fcst_length = model_fcst_length[model_name] # fcstlength in dictionay model_fcst_length

        for vhr in arange(24, fcst_length+12, 12):  # [24, 36, 48, 60, 72, 84]

            initnwp_date = utcdate - datetime.timedelta(hours=vhr)

            cdate_initnwp = initnwp_date.strftime("%Y%m%d%H")  # nwp-mode inittime

            print("#" * 40)
            print(" MET_PostProc_MODE :  " + cdate_initnwp + " ==> + " + str(vhr) + "H  " + cdate_utc)
            print("#" * 40)

            for kth in range(8):  # every

                mode_ps_fname = gv.result_dir + model_name + "/" + cdate_utc + "/" +  \
                                "mode_" + mode_prefix[model_name] + "_" + str(vhr) + "0000L_" +  \
                                cdate_utc[0:8] + "_" + cdate_utc[8:10] + "0000V_240000A_" \
                                + "R" + str(kth+1) + "_T" + str(kth+1) + ".ps"

                mode_png_00p = gv.result_dir + model_name + "/" + cdate_utc + "/" + \
                                 "mode_" + mode_prefix[model_name] + "_" + str(vhr).zfill(3) + "_" + \
                                cdate_utc + "_RT_" + str(kth).zfill(2) + "_00p" + ".png"

                mode_png_04p = gv.result_dir + model_name + "/" + cdate_utc + "/" + \
                               "mode_" + mode_prefix[model_name] + "_" + str(vhr).zfill(3) + "_" + \
                                cdate_utc + "_RT_" + str(kth).zfill(2) + "_01p" + ".png"

                mode_png_des = gv.result_dir + model_name + "/" + cdate_utc + "/" + \
                               "mode_" + mode_prefix[model_name] + "_" + str(vhr).zfill(3) + "_" + \
                                cdate_utc + "_RT_" + str(kth).zfill(2) + "_fin" + ".png"

                cmd = "convert -density 240 " + mode_ps_fname + "[0] " + mode_png_00p + " ; " + \
                      "convert -density 240 " + mode_ps_fname + "[4] " + mode_png_04p + " ; " + \
                      "convert -append " + mode_png_00p + " " + mode_png_04p + " " + mode_png_des

                print(cmd)

                os.system(cmd)

                # print(mode_ps_fname)
                # print(mode_png_fname)



    return

#############################################################




#############################################################


def met_postproc_poinstat(cdate_utc):

    # cdate_utc = "2018062500"

    cyear = cdate_utc[0:4]

    cmon = cdate_utc[4:6]

    cday = cdate_utc[6:8]

    chour = cdate_utc[8:10]

    print(cyear + cmon + cday + chour)

    utcdate = datetime.datetime(int(cyear), int(cmon), int(cday), int(chour))

    # lstdate = utcdate + datetime.timedelta(hours=8)

    print
    print(" =================================== ")
    print

    for model_name in gv.model_dir:

        fcst_length = gv.model_fcst_length[model_name]

        for vhr in arange(24, fcst_length+12, 12):  # [24, 36, 48, 60, 72, 84]

            initnwp_date = utcdate - datetime.timedelta(hours=vhr)

            cdate_initnwp = initnwp_date.strftime("%Y%m%d%H")  # nwp-mode inittime

            print("#" * 40)
            print(" MET_PostProc_pointstat :  " + cdate_initnwp + " ==> + " + str(vhr) + "H  " + cdate_utc)
            print("#" * 40)

            print
            print("#"*15 + " MET Postprogress CSI" + "#"*15)
            print

            init_cdate = cdate_initnwp

            valid_cdate = cdate_utc

            print(init_cdate)

        #    /home/vgdisk02/fcst2018/MET_RESULT/ecmwf/2018062300/point_stat_ECMWF_M4_360000L_20180623_000000V_cts.txt*

            f_ps_name = gv.result_dir + model_name + "//" + valid_cdate + "//" + \
                        "point_stat_" + model_name.upper() + "_M4_" + \
                        str(vhr) + "0000L_" + valid_cdate[0:8] + "_" + valid_cdate[8:10] + "0000V" + \
                        "_cts.txt"

            print(f_ps_name)

            try:
                ps_data = pd.read_csv(f_ps_name, sep="\s+", na_values="NA")
            except:
                print(" File " + f_ps_name + " Error !")
                return

            scores = ["ACC", "FBIAS", "PODY", "POFD", "FAR", "CSI", "GSS", "HSS"]

            col_labels = ps_data["FCST_THRESH"][0:10]

            tabledata = ps_data[scores][0:10]  # 10 for cols, 8 for rows

            # irow = 0
            # for irow in range(10):
            #
            #     # tabledata[irow, :] = [ "%.3f" % x for x in ps_data[scores][0:10] ]
            #
            #     tabledata[irow, :] = [ round(x, 3) for x in ps_data[scores][0:10]]
            #
            #     irow = irow + 1

            fig, ax = plt.subplots(2, 1)

            # ax = figure(1,figsize=(8, 10))

            ax[0].bar(arange(10), tabledata["CSI"], width=0.5, color="darkblue")

            for k in arange(10):

                xpos = k

                if ( isnan( tabledata["CSI"][k] )  ):      # pay attention to nan value
                    ypos = 0.05
                else:
                    ypos = max(tabledata["CSI"][k] + 0.05, 0.05)

                ax[0].text(xpos, ypos, str(round(tabledata["CSI"][k], 2)))

            ax[0].set_ylim(0, 1.0)

            ax[0].set_yticks([round(x, 2) for x in arange(0, 1.1, 0.1)])

            ax[0].set_yticklabels(ax[0].get_yticks(), fontsize=10)

            ax[0].set_xlim(-0.5, 10.5)

            ax[0].set_xticks(arange(10))

            ax[0].set_xticklabels(col_labels, fontsize=10)

            ax[0].set_title( model_name.upper() + " CSI(TS) " + init_cdate + " + " + str(vhr).zfill(3) + \
                             "hr   " + valid_cdate, fontsize=15)

            ax[1].axis("off")

            # tempvar = np.array([round(x, 3) for x in tabledata.flatten()]).reshape(8, 10)

            tempvar = np.array([round(x, 3) for x in np.array(tabledata).flatten()]).reshape(10, 8).transpose()

            # this_table = ax[1].table(cellText=tempvar, rowLabels=scores, colLabels=col_labels, rowColours=["green"] * 8, loc="center")

            print(tabledata)

            this_table = ax[1].table(cellText=tempvar, rowLabels=scores, colLabels=col_labels, rowColours=["green"]*8, loc="center")

            this_table.auto_set_font_size(False)

            this_table.set_fontsize(10)

            plt.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.9, hspace=0.1, wspace=0.3)
            #
            # plt.show()

            plt.savefig( gv.result_dir + model_name + "/" + cdate_utc + "/./met_" + model_name + "_ps_cts_i" + init_cdate + "_v" + valid_cdate + "_" + str(vhr).zfill(3) + ".png")

            close(fig)
