
## -*- coding: utf-8 -*-
from pylab import *

import os

import pandas as pd

import pdb

import datetime


proj_home = "/home/lse/vgdisk02/fcst2018/NMC_MET_TOOLS/"

result_dir = proj_home + "../MET_RESULT/"

model_dir =  ["ecmwf", "gfs", "warms", "pwafs15"]

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

rxx = "r0.1"

cdate_utc_init = "2018050600"

for model_name in model_dir:

    csi_file = file("csi_" + rxx + "_" + model_name + ".dat", "w")

    cyear = cdate_utc_init[0:4]

    cmon = cdate_utc_init[4:6]

    cday = cdate_utc_init[6:8]

    chour = cdate_utc_init[8:10]

    # print(cyear + cmon + cday + chour)

    t1 = datetime.datetime(int(cyear), int(cmon), int(cday), int(chour))

    for iday in range(1):

        t2 = t1 + datetime.timedelta(hours=24 * iday)

        cdate_utc = t2.strftime("%Y%m%d%H")

        # print(cdate_utc)

        for vhr in arange(36, 36+12, 12):  # [24, 36, 48, 60, 72, 84]

            initnwp_date = t2 - datetime.timedelta(hours=vhr)

            cdate_initnwp = initnwp_date.strftime("%Y%m%d%H")  # nwp-mode inittime

            # print("#" * 40)
            # print(" MET_PostProc_pointstat :  " + cdate_initnwp + " ==> + " + str(vhr) + "H  " + cdate_utc)

            init_cdate = cdate_initnwp

            valid_cdate = cdate_utc

            f_ps_name = result_dir + model_name + "//" + valid_cdate + "//" + \
                        "point_stat_" + model_name.upper() + "_M4_" + \
                        str(vhr) + "0000L_" + valid_cdate[0:8] + "_" + valid_cdate[8:10] + "0000V" + \
                        "_cts.txt"

            try:
                ps_data = pd.read_csv(f_ps_name, sep="\s+", na_values="NA")
                print(f_ps_name)

                scores = ["FCST_THRESH", "ACC", "FBIAS", "PODY", "POFD", "FAR", "CSI"]

                col_labels = ps_data["FCST_THRESH"][ th[rxx]:th[rxx]+1 ]

                tabledata = ps_data[scores][ th[rxx]:th[rxx]+1 ]

                csi_data = tabledata["CSI"].values[0]
                
            except:

                print(" File " + f_ps_name + " Error !")

                csi_data = np.nan

            txtbufr = model_name + "  " + cdate_utc + "  " + str(round(csi_data, 4))

            csi_file.write(txtbufr + "\n")

            print(txtbufr)

    csi_file.close()


# cat -b csi_r25_ecmwf.dat  csi_r25_gfs.dat csi_r25_warms.dat csi_r25_pwafs15.dat  > csi_r25.dat
# paste  -d"\t"  csi_r0.1_ecmwf.dat  csi_r0.1_gfs.dat  csi_r0.1_warms.dat csi_r0.1_pwafs15.dat
# cmd = " find " + result_dir + model_name + " -name " + " \"point*360000L*20180[5-8]*_cts.txt\" "  # payattention to regexp




























