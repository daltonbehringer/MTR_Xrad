'''
initial script to concatenate raw aqpi x-band into one simple file
'''

import os
import numpy as np
from netCDF4 import Dataset
import glob


def concat_data(
        fdir,
        var,
        elev,
        site
        ):

        for filename in glob.glob('aqpi*PPI.netcdf*'):
                f = fdir + filename
                nc = Dataset(f, 'r')
        
        fdir = '/Users/daltonbehringer/MTR_data/xband/XEBY/2024/Feb19/'
        f = fdir + 'aqpi.xeby-20240219-224651_3035_2_4_PPI.netcdf.drops'
        nc = Dataset(f, 'r')

        scan_time = nc.time_coverage_end

        refl = nc.variables['CorrReflectivity'][:]
        zdr = nc.variables['CorrDifferentialReflectivity'][:]
        #snr = nc.variables['SignalToNoiseRatio'][:]
        elev = np.round(nc.variables['elevation'][:][1], decimals=0)
        gw = nc.variables['gateWidth'][:]
        #gw = gw/1000
        az = nc.variables['azimuth'][:]
        fg = nc.variables['startRange'][:]
        fg = (fg*-1)

        refl[zdr < 0.] = np.nan
        zdr[zdr < 0.] = np.nan

        refl = np.ma.array(refl, mask=np.isnan(refl))

        gates = np.arange(1, refl.shape[1]+1)
        gates = (gates*gw[1])
        g1, az1 = np.meshgrid(gates, az)

        g1, fg1 = np.meshgrid(gates, fg)
        r = g1+fg1

        x = r * np.cos(np.radians(az1-90))
        y = -r * np.sin(np.radians(az1-90))



