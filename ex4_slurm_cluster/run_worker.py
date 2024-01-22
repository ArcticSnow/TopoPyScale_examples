import os
import sys
import numpy as np
startYearIndex= sys.argv[1]


import pandas as pd
from TopoPyScale import topoclass as tc
from TopoPyScale import topo_export as te
from TopoPyScale import topo_sim as sim
from datetime import datetime
import os
import numpy as np
from matplotlib import pyplot as plt


startTime = datetime.now()
config_file = './config.yml'
mp = tc.Topoclass(config_file)

myyears = np.arange(mp.config.project.start.year, mp.config.project.end.year + 1)
startYear = myyears[int(startYearIndex)-1]
print(startYear)

mp.extract_topo_param()
wdir = mp.config.project.directory
nclust = mp.config.sampling.toposub.n_clusters
epsg = mp.config.dem.epsg
dem_res = mp.config.dem.dem_res
newdir = wdir+"/sim_"+ str(startYear) +"/"

# copy files
import shutil
source_dir = wdir+"/outputs"
destination_dir = newdir+"/outputs"
if os.path.exists(newdir):
        shutil.rmtree(newdir)



shutil.copytree(source_dir, destination_dir)

src = wdir+"/FSM"
dst = newdir+"/FSM"
shutil.copyfile(src, dst)
shutil.copymode(src, dst)

# update path and parameters
mp.config.project.directory =newdir
mp.config.outputs.downscaled = newdir+ '/outputs/downscaled'
mp.config.outputs.path = newdir+ '/outputs'
mp.config.outputs.tmp_path = mp.config.outputs.path + '/tmp'

mp.config.project.start = mp.config.project.start.replace(year=startYear-1)
mp.config.project.start = mp.config.project.start.replace(month=9)
mp.config.project.start = mp.config.project.start.replace(day=1)
mp.config.project.end = mp.config.project.end.replace(year=startYear)
mp.config.project.end = mp.config.project.end.replace(month=8)
mp.config.project.end = mp.config.project.end.replace(day=31)

if os.path.exists("outputs/ds_solar.nc"):
        os.remove("outputs/ds_solar.nc")
mp.compute_horizon()
mp.compute_solar_geometry()
mp.downscale_climate()

mp.to_fsm()

os.chdir(newdir)
# Simulate FSM
for i in range(mp.config.sampling.toposub.n_clusters):
    nsim = "{:0>2}".format(i)
    sim.fsm_nlst(31, newdir+"/outputs/FSM_pt_"+ nsim +".txt", 24)
    sim.fsm_sim(newdir+"/fsm_sims/nlst_FSM_pt_"+ nsim +".txt", "./FSM")
















res= 500

# Simulate FSM
for i in range(nclust):
    nsim = "{:0>2}".format(i)
    sim.fsm_nlst(31, "./outputs/FSM_pt_"+ nsim +".txt", 24)

    # delete all empty forcing files
    #os.system("find . -name 'FSM*.tx' -empty -delete")

    sim.fsm_sim(newdir + "/fsm_sims/nlst_FSM_pt_"+ nsim +".txt", "./FSM")

# delete all empty sim files - why does this happen!
# os.system("find . -name 'sim_FSM*.txt' -empty -delete")
    
# agg data
df = sim.agg_by_var_fsm(var="snd")

grid_stack, lats, lons = sim.topo_map_sim( df, 1, "float32", res)
sim.write_ncdf(newdir, grid_stack, "swe", "mm","32642",500,  df.index.array, lats, lons, "float32",True,  "snow_water_equivalent")


