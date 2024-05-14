'''
initial script to gather raw aqpi x-band for interogration
'''

import numpy as np
from netCDF4 import Dataset

def format_data(
        fdir,
        fname,
        var
        ):

        # for filename in glob.glob('aqpi*PPI.netcdf*'):
        f = fdir + filename
        nc = Dataset(f, 'r')

        scan_time = nc.time_coverage_end

        refl = nc.variables['CorrReflectivity'][:]
        zdr = nc.variables['CorrDifferentialReflectivity'][:]
        cc = nc.variables['CrossPolCorrelation'][:]
        kdp = nc.variables['KDP'][:]
        vel = nc.variables['Velocity'][:]
        elev = np.round(nc.variables['elevation'][:][1], decimals=0)
        gw = nc.variables['gateWidth'][:]
        #gw = gw/1000
        az = nc.variables['azimuth'][:]
        fg = nc.variables['startRange'][:]
        fg = (fg*-1)

        refl[zdr < -10.] = np.nan
        zdr[zdr < -8.] = np.nan
        cc[cc < 0.] = np.nan
        kdp[kdp <-2.] = np.nan
        vel[vel < -99.] = np.nan

        refl = np.ma.array(refl, mask=np.isnan(refl))
        zdr = np.ma.array(zdr, mask=np.isnan(zdr))
        cc = np.ma.array(cc, mask=np.isnan(cc))
        kdp = np.ma.array(kdp, mask=np.isnan(kdp))
        vel = np.ma.array(vel, mask=np.isnan(vel))

        gates = np.arange(1, refl.shape[1]+1)
        gates = (gates*gw[1])
        g1, az1 = np.meshgrid(gates, az)

        g1, fg1 = np.meshgrid(gates, fg)
        r = g1+fg1

        x = r * np.cos(np.radians(az1-90))
        y = -r * np.sin(np.radians(az1-90))

        outvar = var

        return x, y, outvar, scan_time, elev, lat, lon



