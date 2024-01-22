from TopoPyScale import topoclass as tc

#------------------------------------------
print('\n ------------------------------- \n')
print('Toposub Spatial Downscaling Example')
print('\n ------------------------------- \n')

config_file = './config_test.yml'
mp = tc.Topoclass(config_file)

mp.compute_dem_param()
mp.extract_topo_param()
mp.compute_solar_geometry()
mp.compute_horizon()
mp.downscale_climate()
print('---> Test pass for spatial (toposub) downscaling')






