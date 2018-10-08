# -*- coding: utf-8 -*-

# micaps_r24_dir = "H:\\fcst2018\\micaps\\r24\\"

proj_home = "/home/lse/vgdisk02/fcst2018/NMC_MET_TOOLS/"

# nwp_dir = "/home/lse/vgdisk02/nwp_database/"

nwp_dir = "/home/lse/vgdisk02/nwp_database_local/"

obs_dir = "/home/lse/vgdisk02/obs_database/"

micaps_r24_dir = obs_dir +"./micaps/r24/"

qpe_cmorph_dir = obs_dir + "./QPE_CMORPH/"

qpe_nmic_dir = obs_dir + "./qpe_nmic/024h/"

#
# qpe_dir = "H:\\fcst2018\cmorph\\ftp.cpc.ncep.noaa.gov\\precip\\CMORPH_V1.0\\RAW\\0.25deg-DLY_00Z\\"
#
# nwp_ec_dir = "S:\\globalECMWF\\"
#
# nwp_gfs_dir = "S:\\globalNCEP\\"
#
# nwp_eceps_dir = "S:\\ecmfEnsemble\\"
#
# nwp_grapes3km_dir = "S:\\mesoGRAPES3KM\\"
#
# nwp_warms_dir = "S:\\mesoHUANANgrapes9KM\\"
#
# nwp_satsimu_dir = ""
#

nwp_ec_dir = nwp_dir + "globalECMWF/"

nwp_gfs_dir = nwp_dir + "globalNCEP/"

nwp_eceps_dir = nwp_dir + "ecmfEnsemble/"

nwp_grapes3km_dir = nwp_dir + "mesoGRAPES3KM/"

nwp_warms_dir = nwp_dir + "mesoSHANGHAI/"

nwp_ramps_dir = nwp_dir + "meso/"

nwp_satsimu_dir = ""

tempdir = proj_home + "./temp/"

use_ecmwf = True

use_eceps = False

use_gfs = True

use_warms = True

## result directory structure

result_dir = proj_home + "../MET_RESULT/"

model_dir = ["ecmwf", "gfs", "warms"]

mode_prefix = {"ecmwf": "EC_CMORPH", "gfs": "GFS_CMORPH", "warms": "WARMS_CMORPH" }

model_fcst_length = {"ecmwf": 84, "eceps": 84, "gfs": 84, "warms": 48}



## MICAPS GDS_DATA_SERVICE

gds_server = "10.32.8.164"
gds_server_port = 8080


