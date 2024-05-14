'''
Plots a basic PPI of AQPI X-band data
'''

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as colors
import cartopy.crs as ccrs
import pyproj
import glob

from metpy.plots import ctables
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature

from ..utility.format import format_data

matplotlib.rcParams['mathtext.fontset'] = 'dejavusans'
matplotlib.rc('font', family='sans serif')


font = {'family': 'sans serif',
        'color':  'black',
        'weight': 'normal',
        'size': 16,
        }
labelsize = 16

fdir = '/Users/daltonbehringer/MTR_data/xband/XSCR/2024/Mar2/2deg'
var = refl


def plot_ppi(
	fdir,
	var,
	time_format = "%H%M%S",
	title = None,
	y_label = None,
	x_label = None,
	ax = None,
	fig = None,
	tighten = True,
	**kwargs
	):

	x, y, data, time, elev, lat, lon = [], [], [], [], [], [], []

	for fname in glob.glob('/aqpi*PPI.netcdf*'):
		formatted = format_data(fdir, fname, var)
		x.extend = formatted[0]
		y.extend = formatted[1]
		data.extend = formatted[2]
		time.extend = formatted[3]
		elev.extend = formatted[4]
		lat_.extend = formatted[5]
		lon_.extend = formatted[6]

	proj_radar = pyproj.Proj(proj='aeqd', lon_0=lon_, lat_0=lat_)
	lon, lat = proj_radar(x, y, inverse=True)

	fig = plt.figure(figsize=(9,9))
	ax = plt.axes(projection=ccrs.LambertConformal(central_longitude=lon0, central_latitude=lat0))

	if var == 'refl':
		cmap = ctables.registry.get_colortable('NWSReflectivityExpanded')
		mesh = ax.pcolormesh(lon, lat, data, vmin=-36, vmax=80, cmap=cmap,
	                     linewidth=0.000001, edgecolors='face', transform=ccrs.PlateCarree())
	if var == 'zdr':
		cmap = ctables.registry.get_colortable('rainbow')
		mesh = ax.pcolormesh(lon, lat, data, vmin=-8, vmax=8, cmap=cmap,
	                     linewidth=0.000001, edgecolors='face', transform=ccrs.PlateCarree())
	if var == 'cc':
		cmap = ctables.registry.get_colortable('rainbow')
		mesh = ax.pcolormesh(lon, lat, data, vmin=0, vmax=1, cmap=cmap,
	                     linewidth=0.000001, edgecolors='face', transform=ccrs.PlateCarree())
	if var == 'kdp':
		cmap = ctables.registry.get_colortable('rainbow')
		mesh = ax.pcolormesh(lon, lat, data, vmin=-2, vmax=8, cmap=cmap,
	                     linewidth=0.000001, edgecolors='face', transform=ccrs.PlateCarree())
	if var == 'vel':
		cmap = ctables.registry.get_colortable('NWS8bitVel')
		mesh = ax.pcolormesh(lon, lat, data, vmin=-100, vmax=100, cmap=cmap,
	                     linewidth=0.000001, edgecolors='face', transform=ccrs.PlateCarree())

	ax.plot(lon0, lat0, 'rx', markersize=2, transform=ccrs.PlateCarree())

	shp_path = '/Users/daltonbehringer/MTR_data/shapefiles/'
	county_shapes = ShapelyFeature(Reader(shp_path+'Counties.shp').geometries(), ccrs.PlateCarree(), facecolor='none', edgecolor='black')
	ax.add_feature(county_shapes)
	pri_roads_shapes = ShapelyFeature(Reader(shp_path+'tl_2019_us_primaryroads.shp').geometries(), ccrs.PlateCarree(), facecolor='none', edgecolor='orange')
	ax.add_feature(pri_roads_shapes)

	# ax.coastlines()

	plt.colorbar(mesh, shrink=0.8)

