from TopoPyScale import topoclass as tc

#------------------------------------------
print('\n ------------------------------- \n')
print('Point Downscaling Example')
print('\n ------------------------------- \n')

config_file = './config_point.yml'
mq = tc.Topoclass(config_file)
mq.compute_dem_param()
mq.extract_topo_param()
mq.compute_solar_geometry()
mq.compute_horizon()
mq.downscale_climate()
print('---> Exporting downscaled points to Cryogrid formated file')
mq.to_cryogrid()

print('\n ------------------------------- \n')
print('You may use these files to run simulation using the Julia model Cryogrid.jl')
print('\n ------------------------------- \n')
