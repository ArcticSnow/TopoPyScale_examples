from TopoPyScale import topoclass as tc
import glob


#------------------------------------------
print('\n ------------------------------- \n')
print('Toposub Spatial Downscaling Example')
print('\n ------------------------------- \n')

config_file = './config_spatial.yml'
mp = tc.Topoclass(config_file)
mp.get_era5()
mp.compute_dem_param()
mp.extract_topo_param()
mp.compute_solar_geometry()
mp.compute_horizon()
mp.downscale_climate()
print('---> Exporting downscaled clusters to FSM formated file')
mp.to_fsm()

print('\n ------------------------------- \n')
print('You may use these files to run simulation using the Fortran model FSM')
if input('Run FSM? This requires FSM has been compiled. (y/n)') == 'y':
    from TopoPyScale import sim_fsm as sim
    from TopoPyScale import topo_plot as plot
    import matplotlib.pyplot as plt
    
    met_flist = glob.glob("./outputs/FSM_pt_*")
    met_flist.sort()
    
    for nsim, met_file in enumerate(met_flist):
        sim.fsm_nlst(31, met_file, 24)
        
    nlst_flist = glob.glob("./fsm_sims/nlst_FS*")
    nlst_flist.sort()
    
    for nsim, nlst_file in enumerate(nlst_flist):
        sim.fsm_sim(nlst_file, "./FSM")

    # extract GST results(8)
    df = sim.agg_by_var_fsm(var='gst')
    
    df.plot()
    plt.ylabel('GST [$^{o}C$]')
    plt.show()
    
    ds_fsm = sim.to_dataset()
    
    # mapping timeseries to their conresponding pixel location for a single timestep
    plot.map_variable(ds_fsm, mp.toposub.ds_param, time_step=100, var='t_surface')
    plt.show()
    
    # mapping timeseries to their conresponding pixel location for the mean surface temperature
    plot.map_variable(ds_fsm.t_surface.mean(dim='time').to_dataset(), mp.toposub.ds_param)
    plt.title('Mean Surface Temperature')
    plt.show()
    

print('\n ------------------------------- \n')


