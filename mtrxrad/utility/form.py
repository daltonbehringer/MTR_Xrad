'''
initial script to gather raw aqpi x-band for interogration
'''

import numpy as np
from netCDF4 import Dataset

# fdir = '/Users/daltonbehringer/MTR_data/xband/XSCR/2024/Mar2/2deg/'
# fname = 'aqpi.scrz-20240302-020019_107417_21_2_PPI.netcdf.drops'
# var = 'BR'

def format_data(
        f,
        radvar
        ):

        nc = Dataset(f, 'r')

        scan_time = nc.variables['Time'][:]

        if radvar == 'BR':
                data = nc.variables['Reflectivity'][:]
                data[data < -10.] = np.nan
                data = np.ma.array(data, mask=np.isnan(data))
        if radvar == 'ZDR':
                data = nc.variables['DifferentialReflectivity'][:]
                data[data < -8.] = np.nan
                data = np.ma.array(data, mask=np.isnan(data))
        if radvar == 'CC':
                data = nc.variables['CrossPolCorrelation'][:]
                data[data < 0.] = np.nan
                data = np.ma.array(data, mask=np.isnan(data))
        if radvar == 'KDP':
                data = nc.variables['SpecificPhase'][:]
                data[data <-2.] = np.nan
                data = np.ma.array(data, mask=np.isnan(data))
        if radvar == 'BV':
                data = nc.variables['Velocity'][:]
                data[data < -99.] = np.nan
                data = np.ma.array(data, mask=np.isnan(data))

        elev = np.round(nc.variables['Elevation'][:][1], decimals=0)
        lat = nc.Latitude
        lon = nc.Longitude
        gw = nc.variables['GateWidth'][:]
        #gw = gw/1000
        az = nc.variables['Azimuth'][:]
        fg = nc.variables['StartRange'][:]
        fg = (fg*-1)

        gates = np.arange(1, data.shape[1]+1)
        gates = (gates*gw[1])
        g1, az1 = np.meshgrid(gates, az)

        g1, fg1 = np.meshgrid(gates, fg)
        r = g1+fg1

        x = r * np.cos(np.radians(az1-90))
        y = -r * np.sin(np.radians(az1-90))

        return x, y, data, scan_time, elev, lat, lon

