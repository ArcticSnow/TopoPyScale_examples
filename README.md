# TopoPyScale_examples
Set of examples on which to run [TopoPyScale](https://github.com/ArcticSnow/TopoPyScale)

The example `ex1_norway_finse` contains two Jupyter Notebooks available on [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ArcticSnow/TopoPyScale_examples/HEAD)


**WARNINGS**
1. You need a Python VE setup with TopoPyScale installed
2. `cdsapi` credentials must be ready
3. These script will download the climate data from Copernicus ERA5 repository

Contributors:

- Simon Filhol
- Joel Fiddes


## Usage with TopoPyScale

1. Clone the repository
2. modify the `project_dir` in `config.yml` to fit your path
3. Run the pipeline within your relevant virtual environment
```
python pipeline.py
```

Now you may wait for the climate data to download. Downscaling will follow.


## Example 1: Finse in Norway

Folder `ex1_norway_finse`


## Example 2: Retezat Mountain Range in Romania

Folder `ex2_romania_retezat`

## Example 3: Davos in Switzerland

Folder `ex3_switzerland_davos`

## Example 4: SLURM cluster jobs

Folder `ex4_slurm_cluster`

This example is not intended to be run out of the box but as a guidance for those using SLURM based clusters. It will need to be adapted to your situation. If using FSM the executable will need to be compiled on your cluster.

My use case is the the WSL hyperion cluster which uses a slurm based scheduling system. The issue is that nodes are not connected so cannot make use of dask easily (unlike the UIO server for example), There do seem to be ways but I think will need someone cleverer than me to figure that out:

https://jobqueue.dask.org/en/latest/generated/dask_jobqueue.SLURMCluster.html

My approach is to make it possible to distribute a big job (mine is most of the Tian Shan and some of the Pamir) by year to the cluster. This means a couple of things:

1. climate data needs to be independent of the sim directory (ie new climate path variable)
2. 2 new py scripts that van be handled by slurm: **(1) run_master.py** and **(2) run_worker.py**

### **run_master.py**
- runs once
- sets up the the sim

like this:

```
from TopoPyScale import topoclass as tc

config_file = './config.yml'
mp = tc.Topoclass(config_file)
wdir = mp.config.project.directory
mp.compute_dem_param()
mp.extract_topo_param()
mp.toposub.write_landform()
mp.compute_horizon()
```


### **run_worker.py**
- runs many times in parallel using slurm scheduler
-  downscales a single year by accepting a year value as a single argument
- generates a sub directory for each sim eg sim2000 for year 2000
- example below is also ri=unning fsm sims

like this:

```
import sys
import numpy as np
startYearIndex= sys.argv[1]
myyears = np.arange(2000,2023)
startYear = myyears[int(startYearIndex)-1]
print(startYear)

import pandas as pd
from TopoPyScale import topoclass as tc
from TopoPyScale import topo_export as te
from TopoPyScale import topo_sim as sim
#from TopoPyScale import topo_da as da
#from TopoPyScale import topo_utils as ut
from datetime import datetime
import os
import numpy as np
from matplotlib import pyplot as plt


startTime = datetime.now()
config_file = './config.yml'
mp = tc.Topoclass(config_file)
mp.extract_topo_param()
wdir = mp.config.project.directory
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

# update parameters
mp.config.project.directory =newdir
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

```

Finally slurm.sh files handle the scheduling.

### **slurm_master.sh**

Runs run_master.py as a single job, once. The simulation is now setup (climate, dem, TopoSUB/points outputs, horizon)

```
sbatch slurm_master.sh
```

### **slurm_worker.sh**

Runs a single job for every simulation year (solar calc and downscaling plus any simulation with FSM if desired) in parallel on the cluster. These are embarassingly parallel in that they are completely independent jobs. As we parallelise in time even file access is not overlapping (which can cause issues with netcdf climate files and multiple readers).

The following line must be edited to reflect the number of years in your downscaling job, in this case 23.
```
#SBATCH --array=1-23 # this is number of years in downscaling job (23)
```
This numeric ID is provided then as an argument to ```run_worker.py``` and simply indexes a year vector in ```run_worker.py```

Then simply run:
```
sbatch slurm_worker.py
```

## Adding an example site

Add a folder with a DEM and a complete `config.yml` file. To not overload the Github repo with data add in the `.gitignore` file lines to exclude the climate data and outputs such as:

```txt
ex2_romania_retezat/inputs/climate/* 
ex2_romania_retezat/outputs/*

ex1_norway_finse/inputs/climate/*
ex1_norway_finse/outputs/*
```

Be mindful of the size of the input DEM. Github limits to file above 50 Mb.

