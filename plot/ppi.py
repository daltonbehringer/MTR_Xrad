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

from metpy.plots import ctables
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature

from ..utility.radar_locs import get_loc
from ..utility.format import get_data

matplotlib.rcParams['mathtext.fontset'] = 'dejavusans'
matplotlib.rc('font', family='sans serif')


font = {'family': 'sans serif',
        'color':  'black',
        'weight': 'normal',
        'size': 16,
        }
labelsize = 16


def plot_ppi(
	var,
	elev,
	site,
	time_format = "%H%M%S",
	title = None,
	y_label = None,
	x_label = None,
	ax = None,
	fig = None,
	tighten = True,
	**kwargs
	):

	lon_, lat_ = get_loc(site)[0], get_loc(site)[1]

	proj_radar = pyproj.Proj(proj='aeqd', lon_0=lon_, lat_0=lat_)
	lon, lat = proj_radar(x, y, inverse=True)

	fig = plt.figure(figsize=(9,9))
	ax = plt.axes(projection=ccrs.LambertConformal(central_longitude=lon0, central_latitude=lat0))

	cmap = ctables.registry.get_colortable('NWSReflectivityExpanded')

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

