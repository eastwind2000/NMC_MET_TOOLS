# -*- coding: utf-8 -*-

# micaps_r24_dir = "H:\\fcst2018\\micaps\\r24\\"

proj_home = "H:\\fcst2018\\\NMC_MET_TOOLS\\"

micaps_r24_dir = "../database/micaps/r24/"

qpe_dir = "../database/QPE/"

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

nwp_dir = "H:\\fcst2018\\database\\"

nwp_ec_dir =         nwp_dir + "globalECMWF/"

nwp_gfs_dir =        nwp_dir + "globalNCEP/"

nwp_eceps_dir =      nwp_dir + "ecmfEnsemble/"

nwp_grapes3km_dir =  nwp_dir + "mesoGRAPES3KM/"

nwp_warms_dir =      nwp_dir + "mesoSHANGHAI/"

nwp_ramps_dir =      nwp_dir + "meso/"

nwp_satsimu_dir = ""

tempdir = "./temp/"

use_ecmwf = True

use_eceps = True

use_gfs = True

use_warms = True

## result directory structure
result_dir = "../MET_RESULT/"
model_dir = ["ecmwf", "gfs", "warms"]


## Micaps GDS_DATA_SERVICE

gds_server = "10.32.8.164"
gds_server_port = 8080


