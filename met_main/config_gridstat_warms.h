////////////////////////////////////////////////////////////////////////////////
//
// Grid-Stat configuration file.
//
// For additional information, see the MET_BASE/config/README file.
//
////////////////////////////////////////////////////////////////////////////////

//
// Output model name to be written
//
model = "WARMS";

//
// Output description to be written
// May be set separately in each "obs.field" entry
//
desc = "NA";

//
// Output observation type to be written
//
obtype = "CPC_CMORPH";

////////////////////////////////////////////////////////////////////////////////

//
// Verification grid
//
regrid = {
   to_grid    = OBS;
   method     = BILIN;
   width      = 2;
   vld_thresh = 0.5;
   shape      = SQUARE;
}

////////////////////////////////////////////////////////////////////////////////

//
// May be set separately in each "field" entry
//
censor_thresh    = [];
censor_val       = [];
cat_thresh       = [];
cnt_thresh       = [ NA ];
cnt_logic        = UNION;
wind_thresh      = [ NA ];
wind_logic       = UNION;
eclv_points      = 0.05;
nc_pairs_var_str = "";

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
// Verification masking regions
//
mask = {
//   grid = [ "FULL" ];
   poly = [  "China_boundary.poly" ];
        }

////////////////////////////////////////////////////////////////////////////////

//
// Confidence interval settings
//
ci_alpha  = [ 0.10, 0.05 ];

boot = {
   interval = PCTILE;
   rep_prop = 1.0;
   n_rep    = 0;
   rng      = "mt19937";
   seed     = "1";
}

////////////////////////////////////////////////////////////////////////////////

//
// Data smoothing methods
//
interp = {
   field      = FCST;
   vld_thresh = 1.0;
   shape      = SQUARE;

   type = [
      {
         method = NEAREST;
         width  = 1;
      }
   ];
}

////////////////////////////////////////////////////////////////////////////////

//
// Neighborhood methods
//
nbrhd = {
   width      = [ 3, 5 ];
   cov_thresh = [ >=0.5 ];
   vld_thresh = 1.0;
   shape      = SQUARE;
}

////////////////////////////////////////////////////////////////////////////////

//
// Fourier decomposition
//
fourier = {
   wave_1d_beg = [];
   wave_1d_end = [];
}

////////////////////////////////////////////////////////////////////////////////

//
// Statistical output types
//
output_flag = {
   fho    = BOTH;
   ctc    = BOTH;
   cts    = BOTH;
   mctc   = BOTH;
   mcts   = BOTH;
   cnt    = BOTH;
   sl1l2  = BOTH;
   sal1l2 = NONE;
   vl1l2  = NONE;
   val1l2 = NONE;
   vcnt   = NONE;
   pct    = NONE;
   pstd   = NONE;
   pjc    = NONE;
   prc    = NONE;
   eclv   = BOTH;
   nbrctc = BOTH;
   nbrcts = BOTH;
   nbrcnt = BOTH;
   grad   = NONE;
}

//
// NetCDF matched pairs output file
//
nc_pairs_flag   = {
   latlon     = TRUE;
   raw        = TRUE;
   diff       = TRUE;
   climo      = TRUE;
   weight     = FALSE;
   nbrhd      = FALSE;
   fourier    = FALSE;
   gradient   = FALSE;
   apply_mask = TRUE;
}

////////////////////////////////////////////////////////////////////////////////

grid_weight_flag = NONE;
rank_corr_flag   = FALSE;
tmp_dir          = "/tmp";
output_prefix    = "WARMS_CMORPH";
version          = "V7.0";

////////////////////////////////////////////////////////////////////////////////
