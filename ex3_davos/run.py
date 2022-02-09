import pandas as pd
from TopoPyScale import topoclass as tc
from matplotlib import pyplot as plt
from TopoPyScale import topo_sim as sim



# download era5 (should read the ini to supply parameters. Area from a DEM or polygon?
# sparse points method?
#era5.retrieve_era5(product="reanalysis", startDate="2020-01-01", endDate="2020-01-31", eraDir="/home/joel/sim/topoPyscale_paiku/inputs/climate/",latN=29.375, latS=28.125, lonW=85.125, lonE=86.375, step=1, num_threads=10, surf_plev='surf', plevels=None)
#plev=[600, 650, 700, 750, 775, 800, 825, 850, 875, 900, 925, 950, 975, 1000 ]
#era5.retrieve_era5(product="reanalysis", startDate="2020-01-01", endDate="2020-01-31", eraDir="/home/joel/sim/topoPyscale_paiku/inputs/climate/",latN=29.375, latS=28.125, lonW=85.125, lonE=86.375, step=1, num_threads=10, surf_plev='plev', plevels=plev)


# ========= STEP 1 ==========
# Load Configuration
config_file = './config.ini'
mp = tc.Topoclass(config_file)

# Compute parameters of the DEM (slope, aspect, sky view factor)
mp.compute_dem_param()

# ========== STEP 2 ===========
# Extract DEM parameters for points of interest (centroids or physical points)

# ----- Option 1:
# Compute clustering of the input DEM and extract cluster centroids
mp.extract_dem_cluster_param()
# plot clusters
mp.toposub.plot_clusters_map()
mp.toposub.write_landform()
# plot sky view factor
# mp.toposub.plot_clusters_map(var='svf', cmap=plt.cm.viridis)

# ------ Option 2:
# inidicate in the config file the .csv file containing a list of point coordinates (!!! must same coordinate system as DEM !!!)
# mp.extract_pts_param(method='linear',index_col=0)

# ========= STEP 3 ==========
# compute solar geometry and horizon angles
mp.compute_solar_geometry()
mp.compute_horizon()

# ========= STEP 4 ==========
# Perform the downscaling
mp.downscale_climate()

# ========= STEP 5 ==========
# explore the downscaled dataset. For instance the temperature difference between each point and the first one
#(mp.downscaled_pts.t-mp.downscaled_pts.t.isel(point_id=0)).plot()
#plt.show()

# ========= STEP 6 ==========
# Export output to desired format
# mp.to_netcdf()
mp.to_fsm()

# ========= STEP 7 ===========
# Simulate FSM
for i in range(mp.config.n_clusters):
    nsim = "{:0>2}".format(i)
    sim.fsm_nlst(31, "./outputs/FSM_pt_"+ nsim +".txt", 24)
    sim.fsm_sim("./fsm_sims/nlst_FSM_pt_"+ nsim +".txt", "./FSM")

# extract GST results(7)
df = sim.agg_by_var_fsm(7)

# extraxt timeseries average
df_mean = sim.timeseries_means_period(df, mp.config.start_date, mp.config.end_date)

# map to domain grid
sim.topo_map(df_mean)


