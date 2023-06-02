
from TopoPyScale import topoclass as tc
from datetime import datetime
import pandas as pd 




startTime = datetime.now()
config_file = './config.yml'
mp = tc.Topoclass(config_file)


wdir = mp.config.project.directory

mp.compute_dem_param()
mp.extract_topo_param()

listpoints = pd.DataFrame(mp.toposub.df_centroids)
listpoints.to_csv("listpoints.csv")

mp.toposub.write_landform()
mp.compute_horizon()

