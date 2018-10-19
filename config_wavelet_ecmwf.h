////////////////////////////////////////////////////////////////////////////////
//
// Wavelet-Stat configuration file.
//
// For additional information, see the MET_BASE/config/README file.
//
////////////////////////////////////////////////////////////////////////////////

//
// Output model name to be written
//
model = "ECMWF";

//
// Output description to be written
// May be set separately in each "obs.field" entry
//
desc = "NA";

//
// Output observation type to be written
//
obtype = "QPE";

////////////////////////////////////////////////////////////////////////////////

//
// Verification grid
// May be set separately in each "field" entry
//
regrid = {
   to_grid    = OBS;
   method     = NEAREST;
   width      = 1;
   vld_thresh = 0.5;
   shape      = SQUARE;
}



////////////////////////////////////////////////////////////////////////////////

//
// May be set separately in each "field" entry
//
censor_thresh = [];
censor_val    = [];

//
// Forecast and observation fields to be verified
//
fcst = {
   field = [
      {
        name       = "APCP_24";
        level      = [ "A24" ];
         cat_thresh = [ >0.1,>1.0, >5.0, >10.0, >25.0, >50.0, >75.0,  >100.0, >150.0, >200.0 ];
      }
   ];
}
obs = {
   field = [
      {
        name       = "APCP_24";
        level      = [ "A24" ];
         cat_thresh = [ >0.1,>1.0, >5.0, >10.0, >25.0, >50.0, >75.0,  >100.0, >150.0, >200.0 ];
      }
   ];
}


////////////////////////////////////////////////////////////////////////////////

//
// Handle missing data
//
mask_missing_flag = NONE;

////////////////////////////////////////////////////////////////////////////////

//
// Decompose the field into dyadic tiles
//
grid_decomp_flag = AUTO;

tile = {
   width = 0;
   location = [
      {
         x_ll = 0;
         y_ll = 0;
      }
   ];
}

////////////////////////////////////////////////////////////////////////////////

//
// Wavelet to be used for the decomposition
//
wavelet = {
   type   = HAAR;
   member = 2;
}

////////////////////////////////////////////////////////////////////////////////

//
// Statistical output types
//
output_flag = {
   isc = BOTH;
}

//
// NetCDF matched pairs and PostScript output files
//
nc_pairs_flag   = {
   raw    = TRUE;
   diff   = TRUE;
}
ps_plot_flag  = TRUE;

////////////////////////////////////////////////////////////////////////////////

//
// Plotting information
//
met_data_dir = "MET_BASE";

fcst_raw_plot = {
   color_table = "MET_BASE/colortables/wrf_precip2.ctable;
   plot_min = 0.0;
   plot_max = 0.0;
}

obs_raw_plot = {
   color_table = "MET_BASE/colortables/wrf_precip2.ctable";
   plot_min = 0.0;
   plot_max = 0.0;
}

wvlt_plot = {
   color_table = "MET_BASE/colortables/NCL_colortables/BlWhRe.ctable";
   plot_min = -1.0;
   plot_max =  1.0;
}

////////////////////////////////////////////////////////////////////////////////

output_prefix = "EC_QPE";
version = "V7.0";

////////////////////////////////////////////////////////////////////////////////
