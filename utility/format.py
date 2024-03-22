'''
initial script to format raw aqpi x-band
'''

import os
import numpy as np
from netCDF4 import Dataset
import pyproj
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import matplotlib.pyplot as plt
from metpy.plots import ctables

fdir = '/Users/daltonbehringer/MTR_data/xband/XEBY/2024/Feb19/'
f = fdir + 'aqpi.xeby-20240219-224651_3035_2_4_PPI.netcdf.drops'
nc = Dataset(f, 'r')

scan_time = nc.time_coverage_end

lon0, lat0 = -122.062316, 37.815769

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

font = {'family': 'arial',
        'color':  'white',
        'weight': 'normal',
        'size': 12,
        }

x = r * np.cos(np.radians(az1-90))
y = -r * np.sin(np.radians(az1-90))

proj_radar = pyproj.Proj(proj='aeqd', lon_0=lon0, lat_0=lat0)
lon, lat = proj_radar(x, y, inverse=True)

fig = plt.figure(figsize=(9,9))
ax = plt.axes(projection=ccrs.LambertConformal(central_longitude=lon0, central_latitude=lat0))

cmap = ctables.registry.get_colortable('NWSReflectivityExpanded')

# Plot radar data on Cartopy map
mesh = ax.pcolormesh(lon, lat, refl, vmin=-36, vmax=80, cmap=cmap,
                     linewidth=0.000001, edgecolors='face', transform=ccrs.PlateCarree())

ax.plot(lon0, lat0, 'r.', markersize=2, transform=ccrs.PlateCarree())

shp_path = '/Users/daltonbehringer/MTR_data/shapefiles/'
county_shapes = ShapelyFeature(Reader(shp_path+'Counties.shp').geometries(), ccrs.PlateCarree(), facecolor='none', edgecolor='black')
ax.add_feature(county_shapes)
pri_roads_shapes = ShapelyFeature(Reader(shp_path+'tl_2019_us_primaryroads.shp').geometries(), ccrs.PlateCarree(), facecolor='none', edgecolor='orange')
ax.add_feature(pri_roads_shapes)

# ax.coastlines()

plt.colorbar(mesh, shrink=0.8)

plt.show()



