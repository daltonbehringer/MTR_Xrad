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

from ..utility.form import format_data

matplotlib.rcParams['mathtext.fontset'] = 'dejavusans'
matplotlib.rc('font', family='sans serif')

font = {'family': 'sans serif',
        'color':  'black',
        'weight': 'normal',
        'size': 16,
        }
labelsize = 16

def plot_ppi(
	f,
	radvar,
	time_format = "%H%M%S",
	title = None,
	y_label = None,
	x_label = None,
	ax = None,
	fig = None,
	tighten = True,
	**kwargs
	):

	print (f)
	formatted = format_data(f, radvar)
	x = formatted[0]
	y = formatted[1]
	data = formatted[2]
	time = formatted[3]
	elev = formatted[4]
	lat_ = formatted[5]
	lon_ = formatted[6]

	proj_radar = pyproj.Proj(proj='aeqd', lon_0=lon_, lat_0=lat_)
	lon, lat = proj_radar(x, y, inverse=True)

	fig = plt.figure(figsize=(9,9))
	ax = plt.axes(projection=ccrs.LambertConformal(central_longitude=lon_, central_latitude=lat_))

	if radvar == 'BR':
		cmap = ctables.registry.get_colortable('NWSReflectivityExpanded')
		mesh = ax.pcolormesh(lon, lat, data, vmin=-36, vmax=80, cmap=cmap,
	                     linewidth=0.000001, edgecolors='face', transform=ccrs.PlateCarree())
	if radvar == 'ZDR':
		cmap = ctables.registry.get_colortable('rainbow')
		mesh = ax.pcolormesh(lon, lat, data, vmin=-8, vmax=8, cmap=cmap,
	                     linewidth=0.000001, edgecolors='face', transform=ccrs.PlateCarree())
	if radvar == 'CC':
		cmap = ctables.registry.get_colortable('rainbow')
		mesh = ax.pcolormesh(lon, lat, data, vmin=0, vmax=1, cmap=cmap,
	                     linewidth=0.000001, edgecolors='face', transform=ccrs.PlateCarree())
	if radvar == 'KDP':
		cmap = ctables.registry.get_colortable('rainbow')
		mesh = ax.pcolormesh(lon, lat, data, vmin=-2, vmax=8, cmap=cmap,
	                     linewidth=0.000001, edgecolors='face', transform=ccrs.PlateCarree())
	if radvar == 'BV':
		cmap = ctables.registry.get_colortable('NWS8bitVel')
		mesh = ax.pcolormesh(lon, lat, data, vmin=-100, vmax=100, cmap=cmap,
	                     linewidth=0.000001, edgecolors='face', transform=ccrs.PlateCarree())

	ax.plot(lon_, lat_, 'rx', markersize=2, transform=ccrs.PlateCarree())

	shp_path = '/Users/daltonbehringer/MTR_data/shapefiles/'
	county_shapes = ShapelyFeature(Reader(shp_path+'Counties.shp').geometries(), ccrs.PlateCarree(), facecolor='none', edgecolor='black')
	ax.add_feature(county_shapes)
	pri_roads_shapes = ShapelyFeature(Reader(shp_path+'tl_2019_us_primaryroads.shp').geometries(), ccrs.PlateCarree(), facecolor='none', edgecolor='orange')
	ax.add_feature(pri_roads_shapes)

	ax.set_title(time)

	plt.colorbar(mesh, shrink=0.8)

	return fig, ax


