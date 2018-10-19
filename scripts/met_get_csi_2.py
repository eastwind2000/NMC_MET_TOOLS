
## -*- coding: utf-8 -*-
from pylab import *

import os

import pandas as pd

import pdb

import datetime


proj_home = "/home/lse/vgdisk02/fcst2018/NMC_MET_TOOLS/"

result_dir = proj_home + "../MET_RESULT/"

model_dir =  ["ecmwf", "gfs", "warms", "pwafs15"]

model_color = ["blue", "green", "yellow", "purple" ]

# model_dir =  ["ecmwf"]

th = { "r0.1": 0,
       "r1.0": 1,
       "r10": 3,
       "r25": 4,
       "r50": 5,
       "r100": 7,
       "r200": 9 }

# [0, 1] >= 0.1
# [1, 2] >= 1
# [2, 3] >= 5.0
# [3, 4] >= 10.0
# [4, 5] >= 25.0
# [5, 6] >= 50.0
# [6, 7] >= 75.0
# [7, 8] >= 100.
# [8, 9] >= 150
# [9, 10] >= 200

##################################################

# rxx = "r0.1"

cdate_utc_init = "2018070500"

cyear = cdate_utc_init[0:4]

cmon = cdate_utc_init[4:6]

cday = cdate_utc_init[6:8]

chour = cdate_utc_init[8:10]

t1 = datetime.datetime(int(cyear), int(cmon), int(cday), int(chour))

for iday in range(120):

    t2 = t1 + datetime.timedelta(hours= 24 * iday)

    cdate_utc = t2.strftime("%Y%m%d%H")

    # print(cdate_utc)

    csi_data = np.zeros((4, 2, 10))  # for 4-models, 2-vhr hours,  10-class csi-scores
    bias_data = np.zeros((4, 2, 10))  # for 4-models, 2-vhr hours,  10-class bias-scores

    for model_name in model_dir:

        model_index = model_dir.index(model_name)

        for vhr in [24, 36]:  # [24, 36, 48, 60, 72, 84]

            vhr_index = int( (vhr-24)/12 )

            initnwp_date = t2 - datetime.timedelta(hours=vhr)

            cdate_initnwp = initnwp_date.strftime("%Y%m%d%H")  # nwp-mode inittime

            # print(" MET_PostProc_pointstat :  " + cdate_initnwp + " ==> + " + str(vhr) + "H  " + cdate_utc)

            init_cdate = cdate_initnwp

            valid_cdate = cdate_utc

            f_ps_name = result_dir + model_name + "//" + valid_cdate + "//" + \
                            "point_stat_" + model_name.upper() + "_M4_" + \
                            str(vhr) + "0000L_" + valid_cdate[0:8] + "_" + valid_cdate[8:10] + "0000V" + \
                            "_cts.txt"

            print(f_ps_name)

            try:

                ps_data = pd.read_csv(f_ps_name, sep="\s+", na_values="NA")

            except IOError:
                print(" File " + f_ps_name + " Error !")
                csi_data[model_index, vhr_index, :] = np.nan
                bias_data[model_index, vhr_index, :] = np.nan

            else:
                scores = ["FCST_THRESH", "ACC", "FBIAS", "PODY", "POFD", "FAR", "CSI"]
                csi_data[model_index, vhr_index, :] = ps_data["CSI"][0:10].values
                bias_data[model_index, vhr_index, :] = ps_data["FBIAS"][0:10].values


    ########### draw CSI BIAS figs ########################################

    for vhr in [24, 36]:  # [24, 36, 48, 60, 72, 84]

        vhr_index = int((vhr - 24) / 12)

        fig, ax = plt.subplots(2, 1)

        x_offset = 0.15
        y_offset = 0.02
        bar_width = 0.12

        pr_class = [">=0.1", ">=10", ">=25", ">=50", ">=100", ">=200" ]

        np.nan_to_num(csi_data, 0)

        np.nan_to_num(bias_data, 0)

        for imodel in arange(4):
                ax[0].bar(arange(6) + imodel * x_offset, csi_data[imodel, vhr_index, (0, 3, 4, 5, 7, 9)],
                          width=bar_width, label=model_dir[imodel], color=model_color[imodel], tick_label=pr_class )

        for i in arange(6):
            xpos = i + 2 * x_offset
            ypos = csi_data[3, vhr_index, (0, 3, 4, 5, 7, 9)][i]
            if (ypos>0):
                ax[0].text(xpos, ypos+y_offset,  str(round(ypos, 2)), fontsize=10)

        ax[0].set_ylim(0, 1.0)
        ax[0].set_title("Multi-models CSI " + cdate_utc + "  " + str(vhr).zfill(3) + "Fcst" )
        ax[0].legend()

        for imodel in arange(4):
                ax[1].bar(arange(6) + imodel * x_offset, bias_data[imodel, vhr_index, (0, 3, 4, 5, 7, 9)],
                          width=bar_width, label=model_dir[imodel], color=model_color[imodel], tick_label=pr_class )

        for i in arange(6):
            xpos = i + 2 * x_offset
            ypos = bias_data[3, vhr_index, (0, 3, 4, 5, 7, 9)][i]
            if (ypos>0):
                ax[1].text( xpos, ypos+y_offset,  str(round(ypos, 2)), fontsize=10 )

        ax[1].set_ylim(0, 3.0)
        ax[1].set_title("Multi-models BIAS " + cdate_utc + "  " + str(vhr).zfill(3) + "Fcst" )
        ax[1].legend()

        # plt.show()

        fig.subplots_adjust( hspace = 0.5 )

        fig.savefig(result_dir + "csi_"+cdate_utc+"_"+str(vhr).zfill(3)+".png", dpi=300)

        close(fig)





# cat -b csi_r25_ecmwf.dat  csi_r25_gfs.dat csi_r25_warms.dat csi_r25_pwafs15.dat  > csi_r25.dat
# paste  -d"\t"  csi_r0.1_ecmwf.dat  csi_r0.1_gfs.dat  csi_r0.1_warms.dat csi_r0.1_pwafs15.dat
# cmd = " find " + result_dir + model_name + " -name " + " \"point*360000L*20180[5-8]*_cts.txt\" "  # payattention to regexp




























