from TopoPyScale import topoclass as tc

config_file = './config.yml'

# create a topopyscale python object
mp = tc.Topoclass(config_file)

# Downscaling preparation routines
mp.compute_dem_param()
mp.extract_topo_param()
mp.compute_solar_geometry()
mp.compute_horizon()

# Downscaling routine
mp.downscale_climate()

# Export in Cryogrid format
mp.to_cryogrid()

