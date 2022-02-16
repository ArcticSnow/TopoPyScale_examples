from TopoPyScale import topoclass as tc
config_file = './config.yml'
mp = tc.Topoclass(config_file)
mp.compute_dem_param()
mp.extract_topo_param()
mp.compute_solar_geometry()
mp.compute_horizon()
mp.downscale_climate()
mp.to_cryogrid()
