from TopoPyScale import topoclass as tc

#------------------------------------------
# TopoSUB Downscaling Example

config_file = './config_spatial.yml'
mp = tc.Topoclass(config_file)
mp.compute_dem_param()
mp.extract_topo_param()
mp.compute_solar_geometry()
mp.compute_horizon()
mp.downscale_climate()
mp.to_cryogrid()


#------------------------------------------
# Point Downscaling Example

config_file = './config_point.yml'
mq = tc.Topoclass(config_file)
mq.compute_dem_param()
mq.extract_topo_param()
mq.compute_solar_geometry()
mq.compute_horizon()
mq.downscale_climate()
mq.to_cryogrid()