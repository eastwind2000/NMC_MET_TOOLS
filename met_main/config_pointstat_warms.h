////////////////////////////////////////////////////////////////////////////////
//
// Point-Stat configuration file.
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

desc = "WARMS-M4";

////////////////////////////////////////////////////////////////////////////////

//
// Verification grid
//
regrid = {
   to_grid    = NONE;
   method     = NEAREST;
   width      = 1;
   vld_thresh = 0.5;
}

////////////////////////////////////////////////////////////////////////////////

censor_thresh = [];
censor_val    = [];
cnt_thresh    = [ NA ];
cnt_logic     = UNION;
wind_thresh   = [ NA ];
wind_logic    = UNION;

//
// Forecast and observation fields to be verified
//
fcst = {
   message_type = ["ADPSFC", "ADPUPA" ];

   field = [
      {
        name       = "APCP_24";
        level      = [ "A24" ];
        cat_thresh = [ >=0.1, >=1,  >=5.0, >=10.0, >=25.0, >=50.0, >=75.0,  >=100.0,  >=150.0,  >=200.0 ];
      }

     ];

}


obs = {
   message_type = ["ADPSFC"];

   field = [
      {
        name       = "AccPrecip";
        level      = [ "Z2" ];
        cat_thresh = [ >=0.1, >=1,  >=5.0, >=10.0, >=25.0, >=50.0, >=75.0,  >=100.0,  >=150.0,  >=200.0 ];
      }

     ];

}



////////////////////////////////////////////////////////////////////////////////

//
// Point observation filtering options
// May be set separately in each "obs.field" entry
//
sid_exc        = [];
obs_quality    = [];
duplicate_flag = NONE;
obs_summary    = NONE;
obs_percentile = 50;

////////////////////////////////////////////////////////////////////////////////

//
// Climatology mean data
//
climo_mean = {

   file_name = [];
   field     = [];

   regrid = {
      vld_thresh = 0.5;
      method     = NEAREST;
      width      = 1;
   }

   time_interp_method = DW_MEAN;
   match_day          = FALSE;
   time_step          = 21600;
}

////////////////////////////////////////////////////////////////////////////////

//
// Point observation time window
//
 obs_window = {
    beg = -5400;
    end =  5400;
 }

////////////////////////////////////////////////////////////////////////////////

//
// Verification masking regions
//
mask = {
   grid = ["FULL" ];
   poly = [ ];
   sid  = [ ];
}

////////////////////////////////////////////////////////////////////////////////

//
// Confidence interval settings
//
ci_alpha  = [ 0.05 ];

boot = {
   interval = PCTILE;
   rep_prop = 1.0;
   n_rep    = 1000;
   rng      = "mt19937";
   seed     = "1";
}

////////////////////////////////////////////////////////////////////////////////

//
// Interpolation methods
//
interp = {
   vld_thresh = 1.0;

   type = [
      {
         method = NEAREST;
         width  = 1;
      },
      {
         method = MEDIAN;
         width  = 3;
      },
      {
         method = DW_MEAN;
         width  = 3;
      }
   ];
}

////////////////////////////////////////////////////////////////////////////////

//
// HiRA verification method
//
hira = {
   flag       = TRUE;
   width      = [ 2, 3, 4, 5 ];
   vld_thresh = 1.0;
   cov_thresh = [ ==0.25 ];
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
   sal1l2 = BOTH;
   vl1l2  = BOTH;
   val1l2 = BOTH;
   vcnt   = BOTH;
   pct    = NONE;
   pstd   = NONE;
   pjc    = NONE;
   prc    = NONE;
   eclv   = BOTH;
   mpr    = BOTH;
}

////////////////////////////////////////////////////////////////////////////////

rank_corr_flag = TRUE;
tmp_dir        = "/tmp";
output_prefix  = "WARMS_M4";
version        = "V7.0";

////////////////////////////////////////////////////////////////////////////////
