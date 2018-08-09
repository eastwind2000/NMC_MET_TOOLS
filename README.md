
## NMC_MET_TOOLS

### NMC-MET Verification Project

- Provide basic verification products for station and gridding observation.
- Provide Object-Oriented space verifications products.
- Experimental verification products for real-time QPF-operation in National Meteorological Center.
- Python-based project running on Linux-platform.

### 1  Setup MET_TOOLS using docker-container or local-compiled programms

### main executable tools used from MET_TOOLS: 
  
- POINT_STAT for station verification  
- GRID_STAT for grid verification
- ENSEMBLE_STAT for ensemble forecast verification
- MODE for Object-based space verification
- WAVELET  
 
### 2 Setting-up observation and forecast data in NETCDF-format

- Micaps r24-88 precipitation data 
- CMISS Micaps r1jm data ?
- CMISS QPE data
- CMORPH QPE data from dss050.1
> Download single-file: wget -c ftp://ftp.cpc.ncep.noaa.gov/precip/CMORPH_V0.x/RAW/0.25deg-DLY_00Z/2018/201806/CMORPH_V0.x_RAW_0.25deg-DLY_00Z_20180602.gz
> Download directory: wget -c -r -np -k -L -p ftp://ftp.cpc.ncep.noaa.gov/precip/CMORPH_V0.x/RAW/0.25deg-DLY_00Z/2018/201807/
- reforming QPE data to netcdf-format using ascii2nc by python-script

### 3 Setting-up precipitation forecast data from several models in NETCDF-format

- ECMWF
- NCEP
- ECMWF_EPS
- GRAPES-GFS/MESO/3KM
- WARMSII, RMAPES, etc

### 4 Verification Products and post-progress

- Traditional verification scores
- MODE-generated postscript files
- Wavelet decomposition for grid-verification
- Setting up met-viewer(plan)

### 5 Experimental MODE verification products for ECMWF precipition forecast initialized on 2018062712UTC

![MODE_products](https://github.com/eastwind2000/NMC_MET_TOOLS/blob/master/result/mode_test-0.png)
![MODE_products](https://github.com/eastwind2000/NMC_MET_TOOLS/blob/master/result/mode_test-4.png)
![MODE_products](https://github.com/eastwind2000/NMC_MET_TOOLS/blob/master/result/mode_test-1.png)
![MODE_products](https://github.com/eastwind2000/NMC_MET_TOOLS/blob/master/result/mode_test-2.png)
![MODE_products](https://github.com/eastwind2000/NMC_MET_TOOLS/blob/master/result/mode_test-3.png)

### 6 Experimetnal Rscript-generated figs from MET_TOOLS

![R](https://www.r-project.org/Rlogo.png)
- Rscript plot_mpr.R   # for *mpr.txt 
- Rscript plot_cnt.R   # for *_cnt*.txt *.stat
- convert convert -density 300  mpr_plots.pdf mpr_plots.png  # format-transition using ImageMagick command-tools

![Rscript](https://raw.githubusercontent.com/eastwind2000/NMC_MET_TOOLS/master/R_script/mpr_plots-0.png)
![Rscript](https://raw.githubusercontent.com/eastwind2000/NMC_MET_TOOLS/master/R_script/mpr_plots-1.png)
![Rscript](https://raw.githubusercontent.com/eastwind2000/NMC_MET_TOOLS/master/R_script/mpr_plots-2.png)


### 7 Setup met-viewer for MET_TOOLS output 

- setup met-viewer container

>     git clone https://github.com/NCAR/container-dtc-metviewer
>
> #From container-dtc-metviewer/METViewer, build METViewer image.
>
>     cd ./METViewer
>
>     # setup environmental variants in .bashrc
>
>     docker build -t metviewer . # may take a long time
>
>     export MYSQL_DIR=/path/for/mysql/tables 
>
>     export METVIEWER_DIR=/path/for/metviewer/output 
>
>     export METVIEWER_DATA=/path/for/data
>
> #From container-dtc-metviewer, start the containers:
>
> - #It  opens up a shell in the docker environment and point to METViewer home directory
>
>        docker-compose run --rm --service-ports metviewer
>
> - #It  starts the containers in the background
>
>        docker-compose up -d 
>
>    #To open a shell in the docker environment
>
>        docker exec -it metviewer_1 /bin/bash
> - Still have bugs: can not linkup with MySQL - VSDB data.
> 
