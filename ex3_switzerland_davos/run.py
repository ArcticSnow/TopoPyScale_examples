from TopoPyScale import topoclass as tc
from TopoPyScale import topo_sim as sim
from datetime import datetime

startTime = datetime.now()
config_file = './config.yml'
mp = tc.Topoclass(config_file)
mp.compute_dem_param()
mp.extract_topo_param()
mp.toposub.df_centroids.to_csv("listpoints.csv")
mp.toposub.write_landform()
mp.compute_solar_geometry()
mp.compute_horizon()
mp.downscale_climate()
mp.to_fsm()

# Simulate FSM
for i in range(mp.config.sampling.toposub.n_clusters):
    nsim = "{:0>2}".format(i)
    sim.fsm_nlst(31, "./outputs/FSM_pt_"+ nsim +".txt", 24)
    sim.fsm_sim("./fsm_sims/nlst_FSM_pt_"+ nsim +".txt", "./FSM")

# extract GST results(7)
df = sim.agg_by_var_fsm(7)

# extraxt timeseries average
df_mean = sim.timeseries_means_period(df, mp.config.project.start, mp.config.project.end)

# map to domain grid
sim.topo_map(df_mean)

endTime = datetime.now()
print("Runtime = " + (str(endTime-startTime)))
