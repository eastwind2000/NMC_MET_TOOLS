////////////////////////////////////////////////////////////////////////////////
//
// MODE configuration file.
//
// For additional information, see the MET_BASE/config/README file.
//
////////////////////////////////////////////////////////////////////////////////

//
// Output model name to be written
//
model = "GFS";

//
// Output description to be written
//
desc = "GFS_CMORPH";

//
// Output observation type to be written
//
obtype = "CPC_CMORPH_PRCP";

////////////////////////////////////////////////////////////////////////////////

//
// Verification grid
//
regrid = {
   to_grid    = OBS;
   method     = BILIN;
   width      = 2;
   vld_thresh = 0.5;
}

////////////////////////////////////////////////////////////////////////////////

//
// Approximate grid resolution (km)
//
grid_res = 15;

////////////////////////////////////////////////////////////////////////////////

//
// Run all permutations of radius and threshold
//
quilt = FALSE;

//
// Forecast and observation fields to be verified
//
fcst = {
   field = {
      name  = "APCP_24";
      level = "A24";
   }

   censor_thresh     = [];
   censor_val        = [];
   conv_radius       = [   10,   5,    4,    4,      3,    3,    2,    2  ];
   conv_thresh       = [>=0.1, >=5, >=10, >=15, >=25.0, >=50, >=75, >=100 ];
   vld_thresh        = 0.5;
   area_thresh       = >=10.0;
   inten_perc_value  = 100;
   inten_perc_thresh = >=0.0;
   merge_thresh      = >=1.25;
   merge_flag        = NONE;
}

obs = fcst;

obs = {
   field = {
      name  = "APCP_24";
      level = "A24";
   }
}

//
// Handle missing data
//
mask_missing_flag = BOTH;

//
// Match objects between the forecast and observation fields
//
match_flag = MERGE_BOTH;

//
// Maximum centroid distance for objects to be compared
//
max_centroid_dist = 800.0/grid_res;

////////////////////////////////////////////////////////////////////////////////

//
// Verification masking regions
//
mask = {
   grid      = "";
   grid_flag = NONE; // Apply to NONE, FCST, OBS, or BOTH
   poly      = "China_boundary.poly";
   poly_flag = BOTH; // Apply to NONE, FCST, OBS, or BOTH
}

////////////////////////////////////////////////////////////////////////////////

//
// Fuzzy engine weights
//
weight = {
   centroid_dist    = 2.0;
   boundary_dist    = 4.0;
   convex_hull_dist = 0.0;
   angle_diff       = 1.0;
   area_ratio       = 1.0;
   int_area_ratio   = 2.0;
   complexity_ratio = 0.0;
   inten_perc_ratio = 0.0;
   inten_perc_value = 50;
}

////////////////////////////////////////////////////////////////////////////////

//
// Fuzzy engine interest functions
//
interest_function = {

   centroid_dist = (
      (            0.0, 1.0 )
      (  60.0/grid_res, 1.0 )
      ( 600.0/grid_res, 0.0 )
   );

   boundary_dist = (
      (            0.0, 1.0 )
      ( 400.0/grid_res, 0.0 )
   );

   convex_hull_dist = (
      (            0.0, 1.0 )
      ( 400.0/grid_res, 0.0 )
   );

   angle_diff = (
      (  0.0, 1.0 )
      ( 30.0, 1.0 )
      ( 90.0, 0.0 )
   );

   corner   = 0.8;
   ratio_if = (
      (    0.0, 0.0 )
      ( corner, 1.0 )
      (    1.0, 1.0 )
   );

   area_ratio = ratio_if;

   int_area_ratio = (
      ( 0.00, 0.00 )
      ( 0.10, 0.50 )
      ( 0.25, 1.00 )
      ( 1.00, 1.00 )
   );

   complexity_ratio = ratio_if;

   inten_perc_ratio = ratio_if;
}

////////////////////////////////////////////////////////////////////////////////

//
// Total interest threshold for determining matches
//
total_interest_thresh = 0.7;

//
// Interest threshold for printing output pair information
//
print_interest_thresh = 0.0;

////////////////////////////////////////////////////////////////////////////////

//
// Plotting information
//
met_data_dir = "MET_BASE";

fcst_raw_plot = {
   color_table      = "MET_BASE/colortables/met_default.ctable";
   plot_min         = 0.0;
   plot_max         = 0.0;
   colorbar_spacing = 1;
}

obs_raw_plot = {
   color_table      = "MET_BASE/colortables/met_default.ctable";
   plot_min         = 0.0;
   plot_max         = 0.0;
   colorbar_spacing = 1;
}

object_plot = {
   color_table      = "MET_BASE/colortables/mode_obj.ctable";
}

//
// Boolean for plotting on the region of valid data within the domain
//
plot_valid_flag = FALSE;

//
// Plot polyline edges using great circle arcs instead of straight lines
//
plot_gcarc_flag = FALSE;

////////////////////////////////////////////////////////////////////////////////

//
// NetCDF matched pairs, PostScript, and contingency table output files
//
ps_plot_flag    = TRUE;
nc_pairs_flag   = {
   latlon       = TRUE;
   raw          = TRUE;
   object_raw   = TRUE;
   object_id    = TRUE;
   cluster_id   = TRUE;
   polylines    = TRUE;
}
ct_stats_flag   = TRUE;

////////////////////////////////////////////////////////////////////////////////

shift_right = 0;   //  grid squares

////////////////////////////////////////////////////////////////////////////////

output_prefix  = "GFS_CMORPH";
version        = "V7.0";

////////////////////////////////////////////////////////////////////////////////
